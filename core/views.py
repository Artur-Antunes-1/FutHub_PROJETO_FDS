from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone 
from .forms import PeladaForm
from .models import Pelada
from django.contrib.auth.forms import UserCreationForm

def custom_logout(request):
    logout(request)
    messages.success(request, "Você saiu da sua conta com sucesso.")
    return redirect('home')
    
@login_required
def editar_pelada(request, pelada_id):
    pelada = get_object_or_404(Pelada, id=pelada_id)
    if request.user != pelada.organizador:
        return HttpResponseForbidden()

@login_required
def confirmar_presenca(request, pelada_id):
    pelada = get_object_or_404(Pelada, id=pelada_id)
    Presenca.objects.get_or_create(jogador=request.user.jogador, pelada=pelada)
    return redirect('detalhes_pelada', pelada_id=pelada.id)

@login_required
def deletar_pelada(request, pelada_id):
    pelada = get_object_or_404(Pelada, id=pelada_id)
    
    # Verifica se o usuário é o organizador ou superusuário
    if request.user == pelada.organizador or request.user.is_superuser:
        pelada.delete()
        messages.success(request, "Pelada excluída com sucesso!")
    else:
        messages.error(request, "Você não tem permissão para excluir esta pelada.")
    
    return redirect('lista_peladas')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Loga o usuário automaticamente após o registro
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    """
    View personalizada para login de usuários.
    """
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

@login_required
def criar_pelada(request):
    """
    View para criação de novas peladas.
    Requer autenticação do usuário.
    """
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

def lista_peladas(request):
    """
    View para listar todas as peladas agendadas.
    """
    peladas = Pelada.objects.all().order_by('-data_inicial')
    return render(request, 'core/lista_peladas.html', {'peladas': peladas})

@login_required
def detalhes_pelada(request, pelada_id):
    """
    View para mostrar detalhes de uma pelada específica.
    """
    pelada = get_object_or_404(Pelada, pk=pelada_id)
    return render(request, 'core/detalhes_pelada.html', {'pelada': pelada})

def pagina_inicial(request):
    """
    View para a página inicial do site.
    Mostra as próximas peladas agendadas.
    """
    proximas_peladas = Pelada.objects.filter(
        data_inicial__gte=timezone.now().date()
    ).order_by('data_inicial')[:3]
    return render(request, 'core/home.html', {'proximas_peladas': proximas_peladas})