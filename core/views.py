from django.shortcuts import render
from .models import Cliente, Processo

def home(request):
    return render(request, 'core/index.html')

def cadastro(request):
    return render(request, 'core/cadastro.html')

def consulta(request):
    processos = Processo.objects.all()
    return render(request, 'core/consulta.html', {'processos': processos})