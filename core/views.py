from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PeladaForm

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
            pelada.organizador = request.user  # Usuário logado garantido pelo decorator
            pelada.save()
            return redirect('lista_peladas')
    else:
        form = PeladaForm()
    
    return render(request, 'core/pelada_form.html', {'form': form})

def pagina_inicial(request):
    """
    View para a página inicial do site.
    """
    return render(request, 'core/home.html')