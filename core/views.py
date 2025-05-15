from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from uuid import UUID
from django.db.models import Q, Count
from .models import Pelada, Presenca, Jogador, Sorteio, SorteioTime, SorteioJogador
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

    # acesso só de organizador ou participante
    if not (
        pelada.organizador == request.user or
        Presenca.objects.filter(pelada=pelada, jogador=jogador).exists()
    ):
        return HttpResponseForbidden()

    # traz presenças, já puxa Jogador→User e ordena por nível desc, depois username
    presencas = (
        Presenca.objects
        .filter(pelada=pelada)
        .select_related('jogador', 'jogador__usuario')
        .order_by('-nivel_habilidade', 'jogador__usuario__username')
    )

    confirmados = presencas.filter(confirmado=True).count()
    limite = pelada.limite_participantes

    # detecta se existe sorteio salvo no banco
    has_sorteio = Sorteio.objects.filter(pelada=pelada).exists()

    return render(request, 'core/detalhes_pelada.html', {
        'pelada': pelada,
        'presencas': presencas,
        'ja_participa': presencas.filter(jogador=jogador).exists(),
        'confirmado': presencas.filter(jogador=jogador, confirmado=True).exists(),
        'confirmados': confirmados,
        'limite': limite,
        'max_estrelas': range(1, 6),    # 1 a 5
        'has_sorteio': has_sorteio,
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

    pres = list(Presenca.objects.filter(pelada=pelada, confirmado=True).select_related('jogador'))
    if len(pres) != pelada.limite_participantes:
        messages.error(request, f'É necessário ter {pelada.limite_participantes} confirmados.')
        return redirect('detalhes_pelada', pk=pk)

    random.shuffle(pres)
    pres.sort(key=lambda p: p.nivel_habilidade, reverse=True)

    # cria Sorteio
    sorteio = Sorteio.objects.create(pelada=pelada)
    teams = [[] for _ in range(4)]
    pattern = list(range(4)) + list(range(3, -1, -1))
    for p, slot in zip(pres, itertools.cycle(pattern)):
        teams[slot].append(p)

    for idx, jogadores in enumerate(teams):
        total = sum(p.nivel_habilidade for p in jogadores)
        vagas = max(0, pelada.limite_participantes//4 - len(jogadores))
        t = SorteioTime.objects.create(
            sorteio=sorteio,
            nome=f"Time {idx+1}",
            total_estrelas=total,
            vagas=vagas
        )
        for p in jogadores:
            SorteioJogador.objects.create(
                time=t,
                jogador=p.jogador,
                nivel_habilidade=p.nivel_habilidade
            )

    messages.success(request, 'Times sorteados e salvos!')
    return redirect('ver_sorteio', pk=pk)

@login_required
def ver_sorteio(request, pk):
    pelada = get_object_or_404(Pelada, pk=pk)
    # só organizador ou participante confirmado
    is_org = (request.user == pelada.organizador)
    is_part = Presenca.objects.filter(
        pelada=pelada,
        jogador__usuario=request.user,
        confirmado=True
    ).exists()
    if not (is_org or is_part):
        return HttpResponseForbidden()

    # pega último sorteio
    sorteio = pelada.sorteios.order_by('-criado_em').first()
    if not sorteio:
        messages.error(request, 'Nenhum sorteio disponível.')
        return redirect('detalhes_pelada', pk=pk)

    # prepara lista de times com vagas_iter
    times = []
    for t in sorteio.times.all().order_by('nome'):
        t.vagas_iter = range(t.vagas)
        times.append(t)

    return render(request, 'core/sorteio_times.html', {
        'pelada': pelada,
        'times': times,
        'max_estrelas': range(1, 6),
    })

@login_required
def ranking_habilidade(request, pk):
    pelada = get_object_or_404(Pelada, pk=pk)

    presencas = Presenca.objects.filter(pelada=pelada).order_by('-nivel_habilidade')
    niveis = [p.nivel_habilidade for p in presencas]
    media = sum(niveis) / len(niveis) if niveis else 0

    return render(request, 'core/ranking_habilidade.html', {
        'pelada': pelada,
        'presencas': presencas,
        'media_nivel': media,
        'max_estrelas': range(1, 6),
    })

@login_required
def meu_perfil(request):
    jogador = request.user.jogador

    if request.method == 'POST':
        # Exclusão de conta
        if 'excluir_conta' in request.POST:
            auth_logout(request)
            request.user.delete()
            messages.success(request, 'Conta excluída com sucesso.')
            return redirect('home')

        # Atualização de perfil (sem email)
        jogador.nome      = request.POST.get('nome', jogador.nome).strip()
        jogador.posicao   = request.POST.get('posicao', jogador.posicao)
        jogador.perna_boa = request.POST.get('perna_boa', jogador.perna_boa)
        jogador.save()

        messages.success(request, 'Perfil atualizado com sucesso.')
        return redirect('meu_perfil')

    # exibe lista de peladas que participa
    presencas = Presenca.objects.filter(jogador=jogador).select_related('pelada')

    return render(request, 'core/perfil.html', {
        'jogador':    jogador,
        'posicoes':   Jogador.POSICAO_CHOICES,
        'pernas':     Jogador.PERNA_CHOICES,
        'presencas':  presencas,
    })

@login_required
def deletar_conta(request):
    if request.method == 'POST':
        auth_logout(request)
        request.user.delete()
        messages.success(request, 'Conta excluída com sucesso.')
        return redirect('home')
    return render(request, 'core/confirmar_exclusao.html')