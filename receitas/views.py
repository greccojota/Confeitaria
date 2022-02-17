from django.shortcuts import get_list_or_404, get_object_or_404, render
from .models import Receita
 # Create your views here.

def index(request):

    receitas = Receita.objects.order_by('-data_receita').filter(publicada=True)

    dados = {
        'receitas': receitas
    }
    
    return render(request, 'index.html', dados)

def receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)

    dados_receita = {
        'receita': receita
    }

    return render(request, 'receita.html', dados_receita)