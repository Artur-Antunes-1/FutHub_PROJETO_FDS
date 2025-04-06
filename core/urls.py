from django.urls import path
from . import views

urlpatterns = [
    path('peladas/criar/', views.criar_pelada, name='criar_pelada'),
]