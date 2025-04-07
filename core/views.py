from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseForbidden
from django.db import IntegrityError
from uuid import UUID
from django.contrib.auth import login as auth_login
from .models import Pelada, Presenca, Jogador
from .forms import PeladaForm

def home(request):
    return render(request, 'core/home.html')

def get_user_pelada_or_403(request, pk):
    jogador = get_object_or_404(Jogador, usuario=request.user)
    pelada = get_object_or_404(Pelada, pk=pk)
    if jogador not in pelada.participantes.all():
        return HttpResponseForbidden("Você não participa desta pelada.")
    return pelada

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                Jogador.objects.create(nome=user.username, email=user.email, usuario=user)
                login(request, user)
                messages.success(request, 'Conta criada com sucesso.')
                return redirect('home')
            except IntegrityError:
                messages.error(request, 'Já existe um jogador com esse e-mail.')
        else:
            messages.error(request, 'Por favor, verifique os dados fornecidos.')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def lista_peladas(request):
    jogador = get_object_or_404(Jogador, usuario=request.user)
    peladas = Pelada.objects.filter(participantes=jogador)
    return render(request, 'core/lista_peladas.html', {'peladas': peladas})

@login_required
def criar_pelada(request):
    jogador = get_object_or_404(Jogador, usuario=request.user)

    if request.method == 'POST':
        form = PeladaForm(request.POST)
        if form.is_valid():
            pelada = form.save(commit=False)
            pelada.criador = jogador
            pelada.save()
            pelada.participantes.add(jogador)
            return redirect('detalhes_pelada', pk=pelada.pk)
    else:
        form = PeladaForm()

    return render(request, 'core/pelada_form.html', {'form': form})

@login_required
def editar_pelada(request, pk):
    pelada = get_object_or_404(Pelada, pk=pk)
    jogador = get_object_or_404(Jogador, usuario=request.user)

    if pelada.criador != jogador:
        return HttpResponseForbidden("Você não tem permissão para editar essa pelada.")
    
    if request.method == 'POST':
        form = PeladaForm(request.POST, instance=pelada)
        if form.is_valid():
            form.save()
            return redirect('detalhes_pelada', pk=pelada.pk)
    else:
        form = PeladaForm(instance=pelada)
    return render(request, 'core/pelada_form.html', {'form': form})


@login_required
def deletar_pelada(request, pk):
    pelada = get_object_or_404(Pelada, pk=pk)
    jogador = get_object_or_404(Jogador, usuario=request.user)

    if pelada.criador != jogador:
        return HttpResponseForbidden("Você não tem permissão para deletar essa pelada.")

    if request.method == 'POST':
        pelada.delete()
        return redirect('lista_peladas')

    return redirect('detalhes_pelada', pk=pk)


@login_required
def detalhes_pelada(request, pk):
    pelada = get_object_or_404(Pelada, pk=pk)
    jogador = get_object_or_404(Jogador, usuario=request.user)

    if jogador not in pelada.participantes.all():
        return HttpResponseForbidden("Você não participa desta pelada.")
    
    return render(request, 'core/detalhes_pelada.html', {'pelada': pelada})



@login_required
def confirmar_presenca(request, pk):
    pelada = get_object_or_404(Pelada, pk=pk)
    jogador = get_object_or_404(Jogador, email=request.user.email)
    Presenca.objects.get_or_create(pelada=pelada, jogador=jogador, confirmado=True)
    messages.success(request, "Presença confirmada!")
    return redirect('detalhes_pelada', pk=pk)

@login_required
def entrar_com_codigo(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        try:
            uuid_codigo = UUID(codigo.strip())
            pelada = get_object_or_404(Pelada, codigo_acesso=uuid_codigo)
            jogador = get_object_or_404(Jogador, email=request.user.email)
            Presenca.objects.get_or_create(pelada=pelada, jogador=jogador)
            messages.success(request, f"Você entrou na pelada '{pelada.nome}'!")
            return redirect('detalhes_pelada', pk=pelada.pk)
        except (ValueError, Pelada.DoesNotExist):
            messages.error(request, "Código inválido ou pelada não encontrada.")
    return render(request, 'core/entrar_com_codigo.html')

def logout_view(request):
    auth_logout(request)
    return redirect('home')

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email ou senha inválidos.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
