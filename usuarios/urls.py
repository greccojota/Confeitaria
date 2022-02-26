from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('cadastro', views.cadastro, name='cadastro'),
    path('login', views.submit_login, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('logout', views.submit_logout, name='logout'),
    path('cria/receita', views.submit_receita, name='cria_receita')
]