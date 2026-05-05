from django.db import models
import uuid

CARRERAS = [
    ('', 'Seleccione una carrera'),
    ('Bach. Ingeniería en Sistemas', 'Ingeniería en Sistemas'),
    ('Bach. Admin. Empresas. Recursos Humanos', 'Bach. Admin. Empresas. Recursos Humanos'),
    ('Bach. Admin. Empresas. Mercadeo', 'Bach. Admin. Empresas. Mercadeo'),
    ('Bach. Admin. Empresas. Contabilidad', 'Bach. Admin. Empresas. Contabilidad'),
    ('Bach. Sist Info Salud', 'Bach. Sist Info Salud'),
    ('Bach. Enfermería', 'Bach. Enfermería'),
    ('Lic. Derecho', 'Lic. Derecho'),
    ('Lic. Recursos Humanos', 'Lic. Recursos Humanos'),
    ('Lic. Contaduría Pública', 'Lic. Contaduría Pública'),
    ('Lic. Mercadeo', 'Lic. Mercadeo'),
    ('Lic. Enfermería', 'Lic. Enfermería'),
    ('Lic. Educación', 'Lic. Educación'),
]

class Estudiante(models.Model):
    nombre = models.CharField(max_length=255)
    identificacion = models.CharField(max_length=50, unique=True)
    carrera = models.CharField(max_length=255, choices=CARRERAS, default='')
    foto = models.ImageField(upload_to='fotos/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_validez = models.DateField()
    token = models.CharField(max_length=255, unique=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.identificacion})"

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = str(uuid.uuid4())
        super().save(*args, **kwargs)

    @property
    def estado_display(self):
        return 'Activo' if self.activo else 'Inactivo'


class HistorialEscaneo(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='escaneos')
    fecha_hora = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        verbose_name = 'Historial de Escaneo'
        verbose_name_plural = 'Historial de Escaneos'
        ordering = ['-fecha_hora']

    def __str__(self):
        return f"{self.estudiante.nombre} - {self.fecha_hora.strftime('%d/%m/%Y %H:%M')}"
