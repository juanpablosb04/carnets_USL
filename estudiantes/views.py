from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
from datetime import date
from dateutil.relativedelta import relativedelta
from .models import Estudiante, HistorialEscaneo
from .forms import EstudianteForm, LoginForm
from django.db import models
from django.core.paginator import Paginator
import qrcode
import qrcode.image.svg
import io
import base64


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


def generar_qr_base64(url):
    qr = qrcode.QRCode(version=1, box_size=8, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode()


# ─── VERIFICACIÓN PÚBLICA ───────────────────────────────────────────────────

def verificar_carnet(request, token):
    estudiante = get_object_or_404(Estudiante, token=token)

    # Registrar escaneo
    HistorialEscaneo.objects.create(
        estudiante=estudiante,
        ip_address=get_client_ip(request)
    )

    hoy = timezone.now().date()
    vigente = estudiante.fecha_validez >= hoy

    return render(request, 'estudiantes/verificar.html', {
        'estudiante': estudiante,
        'vigente': vigente,
        'hoy': hoy,
    })


def carnet_estudiante(request, token):
    estudiante = get_object_or_404(Estudiante, token=token)
    base_url = request.build_absolute_uri('/')[:-1]
    url_verificacion = f"{base_url}/verificar/{estudiante.token}/"
    qr_base64 = generar_qr_base64(url_verificacion)

    return render(request, 'estudiantes/carnet.html', {
        'estudiante': estudiante,
        'qr_base64': qr_base64,
        'url_verificacion': url_verificacion,
    })


# ─── AUTENTICACIÓN ──────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('admin_panel')

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user and user.is_staff:
            login(request, user)
            return redirect('admin_panel')
        else:
            messages.error(request, 'Credenciales inválidas o sin permisos.')

    return render(request, 'estudiantes/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# ─── PANEL ADMIN ────────────────────────────────────────────────────────────

@login_required(login_url='/login/')
def admin_panel(request):
    estudiantes = Estudiante.objects.all()

    # Filtros
    busqueda = request.GET.get('q', '').strip()
    carrera = request.GET.get('carrera', '')
    estado = request.GET.get('estado', '')

    if busqueda:
        estudiantes = estudiantes.filter(
            models.Q(nombre__icontains=busqueda) |
            models.Q(identificacion__icontains=busqueda)
        )
    if carrera:
        estudiantes = estudiantes.filter(carrera=carrera)
    if estado == 'activo':
        estudiantes = estudiantes.filter(activo=True)
    elif estado == 'inactivo':
        estudiantes = estudiantes.filter(activo=False)

    total = Estudiante.objects.count()
    activos = Estudiante.objects.filter(activo=True).count()
    inactivos = Estudiante.objects.filter(activo=False).count()
    total_filtrados = estudiantes.count()

    # Paginación
    paginator = Paginator(estudiantes, 25)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'estudiantes/admin_panel.html', {
        'estudiantes': page_obj,
        'page_obj': page_obj,
        'total': total,
        'activos': activos,
        'inactivos': inactivos,
        'total_filtrados': total_filtrados,
        'busqueda': busqueda,
        'carrera_sel': carrera,
        'estado_sel': estado,
        'carreras': Estudiante.objects.values_list('carrera', flat=True).distinct().order_by('carrera'),
    })


@login_required(login_url='/login/')
def crear_estudiante(request):
    # Fecha default: hoy + 1 año
    fecha_default = date.today() + relativedelta(years=1)

    if request.method == 'POST':
        form = EstudianteForm(request.POST, request.FILES)
        if form.is_valid():
            estudiante = form.save()
            messages.success(request, f'Estudiante {estudiante.nombre} creado exitosamente.')
            return redirect('admin_panel')
    else:
        form = EstudianteForm(initial={'fecha_validez': fecha_default})

    return render(request, 'estudiantes/form_estudiante.html', {
        'form': form,
        'titulo': 'Crear Estudiante',
        'accion': 'Crear',
    })


@login_required(login_url='/login/')
def editar_estudiante(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)

    if request.method == 'POST':
        form = EstudianteForm(request.POST, request.FILES, instance=estudiante)
        if form.is_valid():
            form.save()
            messages.success(request, f'Estudiante {estudiante.nombre} actualizado.')
            return redirect('admin_panel')
    else:
        # instance=estudiante carga automáticamente la fecha existente
        form = EstudianteForm(instance=estudiante)

    return render(request, 'estudiantes/form_estudiante.html', {
        'form': form,
        'titulo': 'Editar Estudiante',
        'accion': 'Guardar cambios',
        'estudiante': estudiante,
    })


@login_required(login_url='/login/')
def toggle_activo(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    estudiante.activo = not estudiante.activo
    estudiante.save()
    estado = 'activado' if estudiante.activo else 'desactivado'
    messages.success(request, f'Carnet de {estudiante.nombre} {estado}.')
    return redirect('admin_panel')


@login_required(login_url='/login/')
def detalle_estudiante(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    base_url = request.build_absolute_uri('/')[:-1]
    url_verificacion = f"{base_url}/verificar/{estudiante.token}/"
    url_carnet = f"{base_url}/carnet/{estudiante.token}/"
    qr_base64 = generar_qr_base64(url_verificacion)
    escaneos = estudiante.escaneos.all()[:10]

    return render(request, 'estudiantes/detalle_estudiante.html', {
        'estudiante': estudiante,
        'qr_base64': qr_base64,
        'url_verificacion': url_verificacion,
        'url_carnet': url_carnet,
        'escaneos': escaneos,
    })


@login_required(login_url='/login/')
def eliminar_estudiante(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    if request.method == 'POST':
        nombre = estudiante.nombre
        estudiante.delete()
        messages.success(request, f'Estudiante {nombre} eliminado.')
        return redirect('admin_panel')

    return render(request, 'estudiantes/confirmar_eliminar.html', {'estudiante': estudiante})
