from django.shortcuts import render, redirect
from .models import Cliente, Processo

def home(request):
    return render(request, 'core/index.html')

def cadastro(request):
    # Se o formulário for enviado (botão Guardar clicado)
    if request.method == 'POST':
        nome_cliente = request.POST.get('nome')
        numero_processo = request.POST.get('numero')
        status_processo = request.POST.get('status')

        # 1. Cria e guarda o Cliente no banco de dados
        novo_cliente = Cliente.objects.create(nome=nome_cliente)

        # 2. Cria e guarda o Processo associado a esse Cliente
        Processo.objects.create(
            cliente=novo_cliente,
            numero=numero_processo,
            status=status_processo
        )

        # Redireciona para a página de consultas para ver o novo registo
        return redirect('consulta')

    # Se for apenas para aceder à página, mostra o formulário vazio
    return render(request, 'core/cadastro.html')

def consulta(request):
    processos = Processo.objects.all()
    return render(request, 'core/consulta.html', {'processos': processos})