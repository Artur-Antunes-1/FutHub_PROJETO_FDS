from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views

urlpatterns = [
    path('', views.pagina_inicial, name='home'),
    path('peladas/criar/', views.criar_pelada, name='criar_pelada'),
    path('peladas/', views.lista_peladas, name='lista_peladas'),
    path('peladas/<int:pelada_id>/', views.detalhes_pelada, name='detalhes_pelada'),
    
    # URLs de autenticação
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]