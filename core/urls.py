from django.urls import path
from . import views

urlpatterns = [
    # Página inicial
    path('', views.home, name='home'),

    # Autenticação
    path('accounts/login/', views.custom_login, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/register/', views.register_view, name='register'),

    # Peladas
    path('peladas/', views.lista_peladas, name='lista_peladas'),
    path('peladas/criar/', views.criar_pelada, name='criar_pelada'),
    path('peladas/<int:pk>/', views.detalhes_pelada, name='detalhes_pelada'),
    path('peladas/<int:pk>/editar/', views.editar_pelada, name='editar_pelada'),
    path('peladas/<int:pk>/deletar/', views.deletar_pelada, name='deletar_pelada'),
    path('peladas/<int:pk>/presenca/',  views.confirmar_presenca, name='confirmar_presenca'),
    path('peladas/<int:pk>/cancelar/',  views.cancelar_presenca,   name='cancelar_presenca'),
    path('peladas/<int:pk>/gerenciar/', views.gerenciar_pelada,    name='gerenciar_pelada'),
    path('peladas/entrar-com-codigo/', views.entrar_com_codigo, name='entrar_com_codigo'),
    path('peladas/<int:pk>/sortear/', views.sortear_times, name='sortear_times'),
    path('peladas/<int:pk>/ver-sorteio/', views.ver_sorteio, name='ver_sorteio'),
    path('peladas/<int:pk>/ranking/', views.ranking_habilidade, name='ranking_habilidade'),
    path('perfil/', views.meu_perfil, name='meu_perfil'),
    path('deletar-conta/', views.deletar_conta, name='deletar_conta'),
]
