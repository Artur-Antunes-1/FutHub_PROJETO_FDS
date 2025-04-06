from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_inicial, name='home'),
    path('peladas/criar/', views.criar_pelada, name='criar_pelada'),
]