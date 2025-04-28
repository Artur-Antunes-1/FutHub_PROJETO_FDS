from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from uuid import UUID
from django.db.models import Q, Count
from .models import Pelada, Presenca, Jogador
from django.views.decorators.http import require_http_methods
import itertools
import random

# Helper para obter ou criar Jogador ativo
def get_or_create_jogador(user):
    jogador, _ = Jogador.objects.get_or_create(
        usuario=user,
        defaults={'nome': user.username, 'email': user.email}
    )
    return jogador

# Página inicial
def home(request):
    return render(request, 'core/home.html')

@login_required
def lista_peladas(request):
    jogador = get_or_create_jogador(request.user)

    peladas = (
        Pelada.objects
        .annotate(
            user_participa=Count('presenca', filter=Q(presenca__jogador=jogador)),
            confirmados=Count('presenca',  filter=Q(presenca__confirmado=True))
        )
        .filter(user_participa__gt=0)
    )

    participante_em = list(
        Presenca.objects.filter(jogador=jogador)
                        .values_list('pelada_id', flat=True)
    )

    for p in peladas:
        if p.limite_participantes:
            porcentagem = p.confirmados / p.limite_participantes
            p.dashoffset = 213.6 - (porcentagem * 213.6)
        else:
            p.dashoffset = 213.6

    return render(request, 'core/lista_peladas.html', {
        'peladas': peladas,
        'participante_em': participante_em,
    })

@login_required
def detalhes_pelada(request, pk):
    jogador = get_or_create_jogador(request.user)
    pelada = get_object_or_404(Pelada, pk=pk)
    # Apenas organizador ou participante vê
    if not (
        pelada.organizador == request.user or
        Presenca.objects.filter(pelada=pelada, jogador=jogador).exists()
    ):
        return HttpResponseForbidden()

    presencas = Presenca.objects.filter(pelada=pelada).select_related('jogador').order_by('jogador__nome')
    confirmados = presencas.filter(confirmado=True).count()
    limite = pelada.limite_participantes

    # Verifica se há sorteio salvo na sessão
    has_sorteio = f'sorteio_{pelada.pk}' in request.session

    return render(request, 'core/detalhes_pelada.html', {
        'pelada': pelada,
        'presencas': presencas,
        'ja_participa': presencas.filter(jogador=jogador).exists(),
        'confirmado': presencas.filter(jogador=jogador, confirmado=True).exists(),
        'confirmados': confirmados,
        'limite': limite,
        'max_estrelas': range(5),  # para mostrar estrelas
        'has_sorteio': has_sorteio,  # flag para botão "Ver Sorteio"
    })

@login_required
@require_http_methods(["GET", "POST"])
def gerenciar_pelada(request, pk):
    pelada = get_object_or_404(Pelada, pk=pk, organizador=request.user)
    presencas = Presenca.objects.filter(pelada=pelada).select_related('jogador')
    if request.method == 'POST':
        # remoção de jogador
        if 'remover' in request.POST:
            pid = request.POST.get('remover')
            pres = get_object_or_404(Presenca, id=pid, pelada=pelada)
            pres.delete()
            messages.success(request, 'Jogador removido com sucesso.')
            return redirect('gerenciar_pelada', pk=pk)
        # atualização de níveis
        if 'salvar_niveis' in request.POST:
            for pres in presencas:
                nivel = request.POST.get(f'nivel_{pres.id}')
                if nivel and nivel.isdigit():
                    pres.nivel_habilidade = int(nivel)
                    pres.save(update_fields=['nivel_habilidade'])
            messages.success(request, 'Níveis de habilidade atualizados.')
            return redirect('gerenciar_pelada', pk=pk)
    return render(request, 'core/gerenciar_pelada.html', {
        'pelada': pelada,
        'presencas': presencas,
        'niveis': range(1,6),
    })

@login_required
@require_http_methods(["GET", "POST"])
def criar_pelada(request):
    jogador = get_or_create_jogador(request.user)
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        data_inicial = request.POST.get('data_inicial')
        hora = request.POST.get('hora')
        local = request.POST.get('local', '').strip()
        recorrente = request.POST.get('recorrente') == 'on'
        limite = request.POST.get('limite_participantes')
        errors = {}
        if not nome:
            errors['nome'] = 'Este campo é obrigatório.'
        if not data_inicial:
            errors['data_inicial'] = 'Este campo é obrigatório.'
        if not hora:
            errors['hora'] = 'Este campo é obrigatório.'
        if not local:
            errors['local'] = 'Este campo é obrigatório.'
        if not limite or not limite.isdigit() or int(limite) < 1:
            errors['limite_participantes'] = 'Informe um número válido.'
        if errors:
            return render(request, 'core/pelada_form.html', {
                'errors': errors,
                'values': {
                    'nome': nome,
                    'data_inicial': data_inicial,
                    'hora': hora,
                    'local': local,
                    'recorrente': recorrente,
                    'limite_participantes': limite,
                }
            })
        pelada = Pelada.objects.create(
            nome=nome,
            data_inicial=data_inicial,
            hora=hora,
            local=local,
            recorrente=recorrente,
            limite_participantes=int(limite),
            organizador=request.user
        )
        Presenca.objects.create(pelada=pelada, jogador=jogador, confirmado=False)
        return redirect('detalhes_pelada', pk=pelada.pk)
    return render(request, 'core/pelada_form.html', {'values': {}})

@login_required
@require_http_methods(["GET", "POST"])
def editar_pelada(request, pk):
    pelada = get_object_or_404(Pelada, pk=pk, organizador=request.user)
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        data_inicial = request.POST.get('data_inicial')
        hora = request.POST.get('hora')
        local = request.POST.get('local', '').strip()
        recorrente = request.POST.get('recorrente') == 'on'
        limite = request.POST.get('limite_participantes')
        errors = {}
        if not nome:
            errors['nome'] = 'Este campo é obrigatório.'
        if not data_inicial:
            errors['data_inicial'] = 'Este campo é obrigatório.'
        if not hora:
            errors['hora'] = 'Este campo é obrigatório.'
        if not local:
            errors['local'] = 'Este campo é obrigatório.'
        if not limite or not limite.isdigit() or int(limite) < 1:
            errors['limite_participantes'] = 'Informe um número válido.'
        if errors:
            return render(request, 'core/pelada_form.html', {
                'errors': errors,
                'values': {
                    'nome': nome,
                    'data_inicial': data_inicial,
                    'hora': hora,
                    'local': local,
                    'recorrente': recorrente,
                    'limite_participantes': limite,
                },
                'object': pelada
            })
        pelada.nome = nome
        pelada.data_inicial = data_inicial
        pelada.hora = hora
        pelada.local = local
        pelada.recorrente = recorrente
        pelada.limite_participantes = int(limite)
        pelada.save()
        return redirect('detalhes_pelada', pk=pk)
    return render(request, 'core/pelada_form.html', {
        'values': {
            'nome': pelada.nome,
            'data_inicial': pelada.data_inicial,
            'hora': pelada.hora,
            'local': pelada.local,
            'recorrente': pelada.recorrente,
            'limite_participantes': pelada.limite_participantes,
        },
        'object': pelada
    })



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
    pelada = get_object_or_404(Pelada, pk=pk)

    # Verifica se o jogador já está registrado na pelada
    if not Presenca.objects.filter(pelada=pelada, jogador=jogador).exists():
        messages.error(request, 'Entre na pelada com o código antes de confirmar presença.')
        return redirect('detalhes_pelada', pk=pk)

    # Conta quantos já confirmaram presença
    confirmados = Presenca.objects.filter(pelada=pelada, confirmado=True).count()

    # Verifica se o limite foi atingido
    if confirmados >= pelada.limite_participantes:
        messages.error(request, 'O limite de participantes foi atingido. Não é possível confirmar presença.')
        return redirect('detalhes_pelada', pk=pk)

    # Se tudo ok, confirma a presença
    Presenca.objects.update_or_create(
        pelada=pelada,
        jogador=jogador,
        defaults={'confirmado': True}
    )

    messages.success(request, 'Presença confirmada!')
    return redirect('detalhes_pelada', pk=pk)

@login_required
def cancelar_presenca(request, pk):
    jogador = get_or_create_jogador(request.user)
    pelada = get_object_or_404(Pelada, pk=pk)
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
            Presenca.objects.get_or_create(pelada=pelada, jogador=jogador, defaults={'confirmado': False})
            messages.success(request, f'Você entrou na pelada “{pelada.nome}”!')
            return redirect('detalhes_pelada', pk=pelada.pk)
        except Exception:
            messages.error(request, 'Código inválido ou pelada não encontrada.')
    return render(request, 'core/entrar_com_codigo.html')

# Autenticação manual
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('home')
        messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'registration/login.html')

# Registro manual
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        errors = {}
        if not username:
            errors['username'] = 'Este campo é obrigatório.'
        if not password1:
            errors['password1'] = 'Este campo é obrigatório.'
        if password1 != password2:
            errors['password2'] = 'As senhas não coincidem.'
        if User.objects.filter(username=username).exists():
            errors['username'] = 'Este usuário já existe.'
        if errors:
            return render(request, 'registration/register.html', {'errors': errors, 'values': {'username': username}})
        user = User.objects.create_user(username=username, password=password1)
        auth_login(request, user)
        return redirect('home')
    return render(request, 'registration/register.html')

@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('home')

@login_required
def sortear_times(request, pk):
    pelada = get_object_or_404(Pelada, pk=pk)
    if request.user != pelada.organizador:
        return HttpResponseForbidden()

    confirmados = list(Presenca.objects.filter(pelada=pelada, confirmado=True).select_related('jogador'))
    limite = pelada.limite_participantes
    if len(confirmados) != limite:
        messages.error(request, f'É necessário ter exatamente {limite} confirmados.')
        return redirect('detalhes_pelada', pk=pk)

    random.shuffle(confirmados)
    confirmados.sort(key=lambda p: p.nivel_habilidade, reverse=True)

    teams_count = 4
    pattern = list(range(teams_count)) + list(range(teams_count-1, -1, -1))
    pat_cycle = itertools.cycle(pattern)

    times = []
    for i in range(teams_count):
        times.append({'nome': f'Time {i+1}', 'jogadores': [], 'total_estrelas': 0, 'vagas': 0})

    for jogador, slot in zip(confirmados, pat_cycle):
        times[slot]['jogadores'].append(jogador)
        times[slot]['total_estrelas'] += jogador.nivel_habilidade
        if sum(len(t['jogadores']) for t in times) == limite:
            break

    for t in times:
        vagas = max(0, limite//teams_count - len(t['jogadores']))
        t['vagas'] = vagas

    # **Salva em sessão** para “ver depois”
    request.session[f'sorteio_{pelada.pk}'] = [
        {
            'nome': t['nome'],
            'jogadores': [
                {'nome': p.jogador.nome, 'nivel': p.nivel_habilidade}
                for p in t['jogadores']
            ],
            'total_estrelas': t['total_estrelas'],
            'vagas': t['vagas'],
        } for t in times
    ]

    messages.success(request, 'Times sorteados com sucesso!')
    return render(request, 'core/sorteio_times.html', {
        'pelada': pelada,
        'times': times,
        'max_estrelas': range(5),
    })

@login_required
def ver_sorteio(request, pk):
    pelada = get_object_or_404(Pelada, pk=pk)
    if request.user != pelada.organizador:
        return HttpResponseForbidden()

    data = request.session.get(f'sorteio_{pk}')
    if not data:
        messages.error(request, 'Nenhum sorteio realizado ainda.')
        return redirect('detalhes_pelada', pk=pk)

    # Reconstrói objetos simples para template
    times = []
    for t in data:
        jogadores = [type('P',(object,),{'jogador':type('J',(object,),{'nome':j['nome']}),'nivel_habilidade':j['nivel']})()
                     for j in t['jogadores']]
        times.append({
            'nome': t['nome'],
            'jogadores': jogadores,
            'total_estrelas': t['total_estrelas'],
            'vagas_iter': range(t['vagas']),
        })

    return render(request, 'core/sorteio_times.html', {
        'pelada': pelada,
        'times': times,
        'max_estrelas': range(5),
    })