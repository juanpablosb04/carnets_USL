from django.urls import path
from . import views

urlpatterns = [
    # Públicas
    path('verificar/<str:token>/', views.verificar_carnet, name='verificar_carnet'),
    path('carnet/<str:token>/', views.carnet_estudiante, name='carnet_estudiante'),

    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Admin panel
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/crear/', views.crear_estudiante, name='crear_estudiante'),
    path('admin-panel/<int:pk>/', views.detalle_estudiante, name='detalle_estudiante'),
    path('admin-panel/<int:pk>/editar/', views.editar_estudiante, name='editar_estudiante'),
    path('admin-panel/<int:pk>/toggle/', views.toggle_activo, name='toggle_activo'),
    path('admin-panel/<int:pk>/eliminar/', views.eliminar_estudiante, name='eliminar_estudiante'),

    # Raíz redirige al panel
    path('', views.login_view, name='home'),
]
