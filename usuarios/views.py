from email import message
from tkinter import FLAT
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from receitas.models import Receita

def cadastro(request):

    if request.POST:
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        confirmacao_senha = request.POST['password2']

        if not nome.strip():
            return redirect('cadastro')
        if not email.strip():
            return redirect('cadastro')
        if senha != confirmacao_senha:
            return redirect('cadastro')

        if User.objects.filter(email = email).exists():
            print('usuario ja cadastrado!')
            return redirect('cadastro')

        User.objects.create_user(username = nome, email = email, password = senha)
        return redirect('login')

    else:
        return render(request, 'usuarios/cadastro.html')

def submit_login(request):

    if request.POST:
        email = request.POST['email']
        senha = request.POST['senha']

        if User.objects.filter(email = email).exists():
            nome = User.objects.filter(email = email).values_list('username', flat=True).get() #buscando o user do email para autenticar o login

            usuario = authenticate(username = nome, password = senha)

            if usuario is not None:
                login(request, usuario)
                return redirect('dashboard')
            else:
                print('Usuário ou Senha Inválido.')
                #messages.error(request, 'Usuário ou Senha Inválido.')

    return render(request, 'usuarios/login.html')

def submit_logout(request):
    logout(request)
    return redirect('index')

def dashboard(request):
    if request.user.is_authenticated:
        id = request.user.id
        receitas = Receita.objects.order_by('-date_receita').filter(pessoa=id)

        dados = { 
            'receitas' : receitas
        }
        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')

def submit_receita(request):
    if request.POST:
        nome = request.POST['nome_receita']
        ingredientes = request.POST['ingredientes']
        modo_preparo = request.POST['modo_preparo']
        tempo_preparo = request.POST['tempo_preparo']
        rendimento = request.POST['rendimento']
        categoria = request.POST['categoria']
        foto_receita = request.FILES['foto_receita']
        usuario = get_object_or_404(User, pk=request.user.id)
        #id_receita = request.POST.get('id_receita')

        #if id_receita:
        #   Receita.objects.filter(nome = nome, ingredientes = ingredientes, modo_preparo = modo_preparo, tempo_preparo = tempo_preparo, rendimento = rendimento, categoria = categoria, foto_receita = foto_receita)
        
        #else:
        Receita.objects.create(pessoa = usuario, nome = nome, ingredientes = ingredientes, modo_preparo = modo_preparo, tempo_preparo = tempo_preparo, rendimento = rendimento, categoria = categoria, foto_receita = foto_receita)
        
        return redirect('dashboard')
    else:
        return render(request, 'usuarios/cria_receita.html')