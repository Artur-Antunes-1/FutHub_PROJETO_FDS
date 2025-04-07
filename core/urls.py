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
    path('peladas/<int:pelada_id>/', views.detalhes_pelada, name='detalhes_pelada'),
    path('peladas/<int:pelada_id>/editar/', views.editar_pelada, name='editar_pelada'),
    path('peladas/<int:pelada_id>/deletar/', views.deletar_pelada, name='deletar_pelada'),
    path('peladas/<int:pelada_id>/confirmar/', views.confirmar_presenca, name='confirmar_presenca'),
    path('peladas/entrar-com-codigo/', views.entrar_com_codigo, name='entrar_com_codigo'),
]
