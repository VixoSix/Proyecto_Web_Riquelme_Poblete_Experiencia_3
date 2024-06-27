from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .models import Envoltura, Roll, Boleta, detalle_boleta
from productos.carrito import Carrito
from .forms import RollForm, RegistroUserForm,MetodoEntregaForm,EditProfileForm
from django.db import transaction
# Create your views here.

def home(request):
    return render(request, 'home.html')

def carta_view(request):
    envolturas = Envoltura.objects.prefetch_related('roll_set').all()
    return render(request, 'carta.html', {'envolturas': envolturas})

def about(request):
    return render(request, 'about.html')

def contacto(request):
    return render(request, 'contacto.html')


def crear(request):
    if request.method == 'POST':
        rollForm = RollForm(request.POST, request.FILES)
        if rollForm.is_valid():
            rollForm.save()
            return redirect('carta')
    else:
        rollForm = RollForm()

    return render(request, 'crear.html', {'rollForm': rollForm })

def detalle(request, id):
    roll = get_object_or_404(Roll, idRool=id)
    return render(request, 'detalle.html', {'roll': roll})

def modificar(request,id):
    roll = Roll.objects.get(idRool=id)
    datos = {
        'forModificar':RollForm(instance=roll)
    }
    if request.method=='POST':
        formulario = RollForm(request.POST,request.FILES,instance=roll)
        if formulario.is_valid():
            formulario.save()
            return redirect('carta')
    return render(request,'modificar.html',datos)

def eliminar(request,id):
    roll = get_object_or_404(Roll, idRool=id)
    if request.method=='POST':
        if 'elimina' in request.POST:
            roll.delete()
            return redirect('carta')
    return render(request,'eliminar.html',{'roll':roll})


def tienda(request):
    envolturas = Envoltura.objects.prefetch_related('roll_set').all()
    return render(request, 'tienda.html', {'envolturas': envolturas})


def cerrar(request):
    logout(request)
    return redirect('home')

def registrar(request):
    data={
        'form': RegistroUserForm()
    }
    if request.method=="POST":
        formulario = RegistroUserForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"],
                    password=formulario.cleaned_data["password1"])
            login(request,user)
            messages.success(request, '¡Registro exitoso! El usuario ha sido creado correctamente.')
            return redirect('home')
        data["form"]=formulario
    return render(request, 'registration/registrar.html',data)

@login_required
def perfil(request):
    boletas = Boleta.objects.filter(usuario=request.user)
    detalles_boletas = detalle_boleta.objects.filter(id_boleta__in=boletas)

    context = {
        'boletas': boletas,
        'detalles_boletas': detalles_boletas,
    }
    return render(request, 'registration/perfil.html', context)

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado exitosamente.')
            return redirect('perfil')
    else:
        form = EditProfileForm(instance=request.user)

    context = {
        'form': form
    }
    return render(request, 'registration/editarperfil.html', context)




def agregar_producto(request,id):
    carrito_compra= Carrito(request)
    roll = Roll.objects.get(idRool=id)
    carrito_compra.agregar(roll=roll)
    return redirect('tienda')


def eliminar_producto(request, id):
    carrito_compra = Carrito(request)
    roll = get_object_or_404(Roll, idRool=id)
    carrito_compra.eliminar(roll=roll)
    return redirect('tienda')

def restar_producto(request, id):
    carrito_compra= Carrito(request)
    roll = Roll.objects.get(idRool=id)
    carrito_compra.restar(roll=roll)
    return redirect('tienda')

def limpiar_carrito(request):
    carrito_compra= Carrito(request)
    carrito_compra.limpiar()
    return redirect('tienda')

@login_required
def realizar_compra(request):
    carrito = Carrito(request)
    if request.method == "POST":
        form = MetodoEntregaForm(request.POST)
        if form.is_valid():
            metodo_entrega = form.cleaned_data['metodo_entrega']
            boleta = generar_boleta(request, metodo_entrega)
            if boleta:
                messages.success(request, f"Compra realizada con éxito. Número de boleta: {boleta.id_boleta}")
                return redirect('detalle_compra', boleta_id=boleta.id_boleta)
            else:
                messages.error(request, "Hubo un problema al generar la boleta.")
                return redirect('tienda')
    else:
        form = MetodoEntregaForm()

    return render(request, 'compra.html', {"carrito": carrito, "form": form})

def generar_boleta(request, metodo_entrega):
    carrito = Carrito(request)
    productos_agregados = []

    try:
        with transaction.atomic():
            precio_total = 0
            for key, value in carrito.carrito.items():
                producto = Roll.objects.select_for_update().get(idRool=value['roll_id'])

                if producto.stockRoll < value['cantidad']:
                    messages.error(request, f"No hay suficiente stock para {producto.nombreRool}.")
                    return None

                subtotal = value['cantidad'] * float(value['precio'])
                detalle = detalle_boleta(id_boleta=None, id_producto=producto, cantidad=value['cantidad'], subtotal=subtotal)
                productos_agregados.append(detalle)
                precio_total += subtotal

            impuestos = precio_total * 0.19  # 19% de impuestos
            envio = 5000 if metodo_entrega == 'envio' else 0  # Costo de envío si se selecciona envío a domicilio
            usuario = request.user

            boleta = Boleta(total=precio_total + impuestos + envio, impuestos=impuestos, envio=envio, usuario=usuario)
            boleta.save()

            for detalle in productos_agregados:
                detalle.id_boleta = boleta
                detalle.save()

            for key, value in carrito.carrito.items():
                producto = Roll.objects.get(idRool=value['roll_id'])
                producto.stockRoll -= value['cantidad']
                producto.save()

            carrito.limpiar()
            return boleta

    except Exception as e:
        print(f"Error al generar boleta: {str(e)}")
        messages.error(request, "Hubo un problema al generar la boleta.")
        return None

def detalle_compra(request, boleta_id):
    boleta = Boleta.objects.get(id_boleta=boleta_id)
    detalles = detalle_boleta.objects.filter(id_boleta=boleta)

    return render(request, 'detallecarrito.html', {
        'boleta': boleta,
        'detalles': detalles,
        'usuario': boleta.usuario,
    })