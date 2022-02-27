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

        if valida_campo(nome):
            messages.error(request, 'Por favor, preencha o Nome de Usuário.')
            return redirect('cadastro')
        if valida_campo(email):
            messages.error(request, 'Por favor, preencha o Email de Usuário.')
            return redirect('cadastro')
        if valida_senha(senha, confirmacao_senha):
            messages.error(request, 'ATENÇÃO: Senhas diferentes.')
            return redirect('cadastro')

        if User.objects.filter(email = email).exists():
            messages.warning(request, 'ATENÇÃO: Email já cadastrado')
            return redirect('cadastro')
        if User.objects.filter(username = nome).exists():
            messages.warning(request, 'ATENÇÃO: Nome já cadastrado')
            return redirect('cadastro')

        usuario = User.objects.create_user(username = nome, email = email, password = senha)
        usuario.save()
        messages.success(request, 'Usuário cadastrado com sucesso.')
        return redirect('login')

    else:
        return render(request, 'usuarios/cadastro.html')

def submit_login(request):

    if request.POST:
        email = request.POST['email']
        senha = request.POST['senha']

        if valida_campo(email) or valida_campo(senha):
            messages.error(request, 'ATENÇÃO: Campos vazios.')
        else:
            if User.objects.filter(email = email).exists():
                nome = User.objects.filter(email = email).values_list('username', flat=True).get() #buscando o user do email para autenticar o login

                usuario = authenticate(username = nome, password = senha)

                if usuario is not None:
                    login(request, usuario)
                    return redirect('dashboard')
                else:
                    messages.error(request, 'ATENÇÃO: Senha Inválida.')
            else:
                messages.error(request, 'ATENÇÃO: Email Inválido.')

    return render(request, 'usuarios/login.html')

def submit_logout(request):
    logout(request)
    return redirect('index')

def dashboard(request):
    if request.user.is_authenticated:
        id = request.user.id
        receitas = Receita.objects.order_by('-data_receita').filter(pessoa=id)

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
        receita = Receita.objects.create(pessoa = usuario, nome = nome, ingredientes = ingredientes, modo_preparo = modo_preparo, tempo_preparo = tempo_preparo, rendimento = rendimento, categoria = categoria, foto_receita = foto_receita)
        receita.save()
        return redirect('dashboard')
    else:
        return render(request, 'usuarios/cria_receita.html')

def valida_campo(campo):
    return not campo.strip()

def valida_senha(x, y):
    return x != y