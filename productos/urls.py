from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home ,name='home'),
    path('about/', views.about, name='about'),
    path('carta/', views.carta_view, name='carta'),
    path('crear/', views.crear, name="crear"),
    path('detalle/<id>/', views.detalle, name="detalle"),
    path('modificar/<id>/', views.modificar, name="modificar"),
    path('eliminarProd/<id>/', views.eliminar, name="eliminarProd"),
    path('contacto/', views.contacto, name='contacto'),


    path('registrar/', views.registrar, name="registrar"),
    path('logout/', views.cerrar, name="cerrar"),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),


    path('tienda/',views.tienda, name="tienda"),
    path('agregar/<id>', views.agregar_producto, name='agregar'),
    path('eliminar/<id>', views.eliminar_producto, name='eliminar'),
    path('restar/<id>', views.restar_producto, name='restar'),
    path('limpiar/', views.limpiar_carrito, name='limpiar'),
    path('realizar_compra/', views.realizar_compra, name='realizar'),
    path('detalle_compra/<int:boleta_id>/', views.detalle_compra, name='detalle_compra'),
]
