# carrito.py
from django.contrib import messages # type: ignore
from productos.models import Roll


class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            carrito = self.session["carrito"] = {}
        self.carrito = carrito

    def agregar(self, roll):
        roll_id = str(roll.idRool)
        if roll.stockRoll <= 0:
            messages.success(self.request, f"Sin Stock en el producto seleccionado")
            return
        if roll_id not in self.carrito:
            self.carrito[roll.idRool] = {
                "roll_id": roll.idRool,
                "nombre": roll.nombreRool,
                "descripcion": roll.descripcionRool,
                "imagen":roll.imagenRool.url,
                "precio": str(roll.precioRoll),
                "cantidad": 1,
                "total": roll.precioRoll,
            }
        else:
            self.carrito[roll_id]["cantidad"] += 1
            self.carrito[roll_id]["total"] += roll.precioRoll

        
        roll.stockRoll -= 1
        roll.save()
        
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def eliminar(self, roll):
        roll_id = str(roll.idRool)
        if roll_id in self.carrito:
            roll.stockRoll += self.carrito[roll_id]["cantidad"]
            roll.save()
            del self.carrito[roll_id]
            self.guardar_carrito()


    def restar(self, roll):
        roll_id = str(roll.idRool)
        if roll_id in self.carrito:
            self.carrito[roll_id]["cantidad"] -= 1
            self.carrito[roll_id]["total"] -= roll.precioRoll
            roll.stockRoll += 1
            roll.save()
            if self.carrito[roll_id]["cantidad"] <= 0:
                self.eliminar(roll)
            else:
                self.guardar_carrito()


    def limpiar(self):
        for roll_id in self.carrito:
            roll = Roll.objects.get(idRool=roll_id)
            roll.stockRoll += self.carrito[roll_id]["cantidad"]
            roll.save()
        self.session["carrito"] = {}
        self.session.modified = True

