from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views

urlpatterns = [
    path('', views.pagina_inicial, name='home'),
    path('peladas/criar/', views.criar_pelada, name='criar_pelada'),
    path('peladas/', views.lista_peladas, name='lista_peladas'),
    path('peladas/<int:pelada_id>/', views.detalhes_pelada, name='detalhes_pelada'),
    path('peladas/<int:pelada_id>/deletar/', views.deletar_pelada, name='deletar_pelada'),
    path('peladas/<int:pelada_id>/editar/', views.editar_pelada, name='editar_pelada'),
    path('peladas/<int:pelada_id>/confirmar/', views.confirmar_presenca, name='confirmar_presenca'),
    
    # URLs de autenticação
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', custom_logout, name='logout'),
    path('accounts/register/', views.register_view, name='register'),
]