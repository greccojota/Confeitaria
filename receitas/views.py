from django.shortcuts import render
 # Create your views here.

def index(request):

    receitas = {
        1:'Bolo de Chocolate',
        2:'Bolo de Laranja',
        3:'Bolo de Iogurte',
        4:'Bolo de Milho'
    }

    dados = {
        'nome_receitas': receitas
    }

    return render(request, 'index.html', dados)

def receita(request):
    return render(request, 'receita.html')