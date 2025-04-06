from django.shortcuts import render, redirect
from .forms import PeladaForm

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

def pagina_inicial(request):
    return render(request, 'core/home.html')