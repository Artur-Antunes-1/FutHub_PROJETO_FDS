from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone 
from .forms import PeladaForm
from .models import Pelada  

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