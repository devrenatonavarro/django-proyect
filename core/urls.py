from django.urls import path
from . import views

urlpatterns = [
    # URLs públicas (clientes)
    path('', views.index, name='index'),
    path('ubicacion/', views.ubicacion, name='ubicacion'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('agregar-carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/actualizar/<int:detalle_id>/', views.actualizar_cantidad_carrito, name='actualizar_cantidad_carrito'),
    path('carrito/eliminar/<int:detalle_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('finalizar-compra/', views.finalizar_compra, name='finalizar_compra'),
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
    path('perfil/', views.perfil, name='perfil'),
    
    # URLs de gestión interna (personal)
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/pedidos/', views.admin_pedidos, name='admin_pedidos'),
    path('admin/pedidos/<int:pedido_id>/cambiar-estado/', views.admin_cambiar_estado_pedido, name='admin_cambiar_estado_pedido'),
    path('admin/pedidos/<int:pedido_id>/asignar-repartidor/', views.admin_asignar_repartidor, name='admin_asignar_repartidor'),
    path('admin/pedidos/<int:pedido_id>/eliminar/', views.admin_eliminar_pedido, name='admin_eliminar_pedido'),
    path('admin/reportes/ventas/', views.admin_reportes_ventas, name='admin_reportes_ventas'),
    path('admin/productos/', views.admin_productos, name='admin_productos'),
    path('admin/productos/crear/', views.admin_crear_producto, name='admin_crear_producto'),
    path('admin/productos/<int:producto_id>/editar/', views.admin_editar_producto, name='admin_editar_producto'),
    path('admin/productos/<int:producto_id>/eliminar/', views.admin_eliminar_producto, name='admin_eliminar_producto'),
    path('admin/productos/<int:producto_id>/toggle/', views.admin_toggle_producto, name='admin_toggle_producto'),
    path('admin/mis-entregas/', views.admin_mis_entregas, name='admin_mis_entregas'),
    path('admin/usuarios/', views.admin_usuarios, name='admin_usuarios'),
    path('admin/usuarios/crear/', views.admin_crear_usuario, name='admin_crear_usuario'),
    path('admin/usuarios/<int:usuario_id>/editar/', views.admin_editar_usuario, name='admin_editar_usuario'),
    path('admin/usuarios/<int:usuario_id>/eliminar/', views.admin_eliminar_usuario, name='admin_eliminar_usuario'),
]
