from django.contrib import admin
from .models import Estudiante, HistorialEscaneo


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'identificacion', 'activo', 'fecha_validez', 'fecha_creacion']
    list_filter = ['activo', 'fecha_validez']
    search_fields = ['nombre', 'identificacion']
    readonly_fields = ['token', 'fecha_creacion', 'fecha_actualizacion']


@admin.register(HistorialEscaneo)
class HistorialEscaneoAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'fecha_hora', 'ip_address']
    list_filter = ['fecha_hora']
    readonly_fields = ['estudiante', 'fecha_hora', 'ip_address']
