from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone 
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseForbidden

from .forms import PeladaForm
from .models import Pelada, Presenca, Jogador

def custom_logout(request):
    logout(request)
    messages.success(request, "Você saiu da sua conta com sucesso.")
    return redirect('home')

def pagina_inicial(request):
    proximas_peladas = Pelada.objects.filter(
        data_inicial__gte=timezone.now().date()
    ).order_by('data_inicial')[:3]
    return render(request, 'core/home.html', {'proximas_peladas': proximas_peladas})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuário ou senha incorretos')
    
    return render(request, 'core/login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Jogador.objects.create(nome=user.username, email=user.email)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def criar_pelada(request):
    if request.method == 'POST':
        form = PeladaForm(request.POST)
        if form.is_valid():
            pelada = form.save(commit=False)
            pelada.organizador = request.user
            pelada.save()
            return redirect('lista_peladas')
    else:
        form = PeladaForm()
    
    return render(request, 'core/pelada_form.html', {'form': form})

@login_required
def editar_pelada(request, pelada_id):
    pelada = get_object_or_404(Pelada, id=pelada_id)

    if request.user != pelada.organizador:
        return HttpResponseForbidden("Você não tem permissão para editar esta pelada.")

    if request.method == 'POST':
        form = PeladaForm(request.POST, instance=pelada)
        if form.is_valid():
            form.save()
            messages.success(request, "Pelada atualizada com sucesso!")
            return redirect('detalhes_pelada', pelada_id=pelada.id)
    else:
        form = PeladaForm(instance=pelada)

    return render(request, 'core/pelada_form.html', {'form': form, 'object': pelada})

def lista_peladas(request):
    if request.user.is_authenticated:
        peladas = Pelada.objects.filter(
            models.Q(organizador=request.user) |
            models.Q(participantes=request.user)
        ).distinct().order_by('-data_inicial')
    else:
        peladas = Pelada.objects.none()
    
    return render(request, 'core/lista_peladas.html', {'peladas': peladas})

@login_required
def detalhes_pelada(request, pelada_id):
    pelada = get_object_or_404(Pelada, pk=pelada_id)
    return render(request, 'core/detalhes_pelada.html', {'pelada': pelada})

@login_required
def confirmar_presenca(request, pelada_id):
    pelada = get_object_or_404(Pelada, id=pelada_id)
    jogador = Jogador.objects.get(email=request.user.email)
    Presenca.objects.get_or_create(jogador=jogador, pelada=pelada)
    return redirect('detalhes_pelada', pelada_id=pelada.id)

@login_required
def deletar_pelada(request, pelada_id):
    pelada = get_object_or_404(Pelada, id=pelada_id)
    
    if request.user == pelada.organizador or request.user.is_superuser:
        pelada.delete()
        messages.success(request, "Pelada excluída com sucesso!")
    else:
        messages.error(request, "Você não tem permissão para excluir esta pelada.")
    
    return redirect('lista_peladas')

@login_required
def entrar_com_codigo(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        try:
            pelada = Pelada.objects.get(codigo_acesso=codigo)
            jogador = Jogador.objects.get(email=request.user.email)
            Presenca.objects.get_or_create(jogador=jogador, pelada=pelada)
            return redirect('detalhes_pelada', pelada_id=pelada.id)
        except Pelada.DoesNotExist:
            messages.error(request, "Código inválido ou pelada não encontrada")
    
    return render(request, 'core/entrar_com_codigo.html')
