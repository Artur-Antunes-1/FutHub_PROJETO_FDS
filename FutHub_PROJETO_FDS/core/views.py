from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseForbidden
from django.db import IntegrityError
from uuid import UUID
from django.db.models import Q
from .models import Pelada, Presenca, Jogador
from .forms import PeladaForm

# Helper para obter ou criar Jogador ativo

def get_or_create_jogador(user):
    jogador, _ = Jogador.objects.get_or_create(
        usuario=user,
        defaults={'nome': user.username, 'email': user.email}
    )
    return jogador


def home(request):
    return render(request, 'core/home.html')

@login_required
def lista_peladas(request):
    jogador = get_or_create_jogador(request.user)

    peladas = Pelada.objects.filter(
        Q(presenca__jogador=jogador) |
        Q(organizador=request.user)
    ).distinct()

    participante_em = peladas.values_list('id', flat=True)
    return render(request, 'core/lista_peladas.html', {
        'peladas': peladas,
        'participante_em': list(participante_em)
    })

@login_required
def criar_pelada(request):
    jogador = get_or_create_jogador(request.user)
    if request.method == 'POST':
        form = PeladaForm(request.POST)
        if form.is_valid():
            pelada = form.save(commit=False)
            pelada.organizador = request.user
            pelada.save()
            Presenca.objects.create(pelada=pelada, jogador=jogador, confirmado=False)
            return redirect('detalhes_pelada', pk=pelada.pk)
    else:
        form = PeladaForm()
    return render(request, 'core/pelada_form.html', {'form': form})

@login_required
def detalhes_pelada(request, pk):
    jogador = get_or_create_jogador(request.user)
    pelada  = get_object_or_404(Pelada, pk=pk)

    # só organiza­dor ou quem já está na pelada vê
    if not (
        pelada.organizador == request.user or
        Presenca.objects.filter(pelada=pelada, jogador=jogador).exists()
    ):
        return HttpResponseForbidden()

    presencas = (
        Presenca.objects
        .filter(pelada=pelada)
        .select_related('jogador')
        .order_by('jogador__nome')
    )
    # 👉 AQUI adicionamos a contagem de confirmados
    confirmados = presencas.filter(confirmado=True).count()
    limite = pelada.limite_participantes

    return render(
        request,
        'core/detalhes_pelada.html',
        {
            'pelada': pelada,
            'presencas': presencas,
            'ja_participa': presencas.filter(jogador=jogador).exists(),
            'confirmado': presencas.filter(jogador=jogador, confirmado=True).exists(),
            'confirmados': confirmados,
            'limite': limite,
        },
    )

@login_required
def editar_pelada(request, pk):
    pelada = get_object_or_404(Pelada, pk=pk, organizador=request.user)
    if request.method == 'POST':
        form = PeladaForm(request.POST, instance=pelada)
        if form.is_valid():
            form.save()
            return redirect('detalhes_pelada', pk=pk)
    else:
        form = PeladaForm(instance=pelada)
    return render(request, 'core/pelada_form.html', {'form': form})

@login_required
def deletar_pelada(request, pk):
    pelada = get_object_or_404(Pelada, pk=pk, organizador=request.user)
    if request.method == 'POST':
        pelada.delete()
        return redirect('lista_peladas')
    return redirect('detalhes_pelada', pk=pk)

@login_required
def confirmar_presenca(request, pk):
    jogador = get_or_create_jogador(request.user)
    pelada  = get_object_or_404(Pelada, pk=pk)

    # impede confirmação se o usuário não é participante
    if not Presenca.objects.filter(pelada=pelada, jogador=jogador).exists():
        messages.error(request, 'Entre na pelada com o código antes de confirmar presença.')
        return redirect('detalhes_pelada', pk=pk)

    Presenca.objects.update_or_create(
        pelada=pelada,
        jogador=jogador,
        defaults={'confirmado': True},
    )
    messages.success(request, 'Presença confirmada!')
    return redirect('detalhes_pelada', pk=pk)

@login_required
def cancelar_presenca(request, pk):
    jogador = get_or_create_jogador(request.user)
    pelada  = get_object_or_404(Pelada, pk=pk)

    presenca = Presenca.objects.filter(pelada=pelada, jogador=jogador).first()
    if not presenca:
        messages.error(request, 'Você não está inscrito nesta pelada.')
    else:
        presenca.confirmado = False
        presenca.save(update_fields=['confirmado'])
        messages.success(request, 'Presença cancelada.')

    return redirect('detalhes_pelada', pk=pk)


@login_required
def entrar_com_codigo(request):
    jogador = get_or_create_jogador(request.user)

    if request.method == 'POST':
        codigo = request.POST.get('codigo_acesso', '').strip()
        try:
            uuid_codigo = UUID(codigo)
            pelada = get_object_or_404(Pelada, codigo_acesso=uuid_codigo)

            Presenca.objects.get_or_create(
                pelada=pelada,
                jogador=jogador,
                defaults={'confirmado': False},
            )

            messages.success(request, f'Você entrou na pelada “{pelada.nome}”!')
            return redirect('detalhes_pelada', pk=pelada.pk)

        except Exception:
            messages.error(request, 'Código inválido ou pelada não encontrada.')

    return render(request, 'core/entrar_com_codigo.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()               # ← o signal já cria Jogador
            auth_login(request, user)
            return redirect('home')
        messages.error(request, 'Verifique os dados.')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
        messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('home')