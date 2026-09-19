from django.shortcuts import render, redirect
from .models import Cliente, Processo

def home(request):
    return render(request, 'core/index.html')

def cadastro(request):
    if request.method == 'POST':
        # Captura os dados do formulário HTML
        nome_cliente = request.POST.get('nome')
        cpf_cliente = request.POST.get('cpf')
        n_processo = request.POST.get('numero')
        status_proc = request.POST.get('status')

        # 1. Cria ou encontra o Cliente. Se for novo, preenche os campos obrigatórios da base de dados.
        cliente_obj, created = Cliente.objects.get_or_create(
            cpf=cpf_cliente,
            defaults={
                'nome': nome_cliente,
                'cep': '00000000',
                'endereco': 'Não informado',
                'cidade': 'Não informada'
            }
        )

        # 2. Cria o Processo usando o nome exato "numero_processo" e adiciona uma "descricao" padrão
        Processo.objects.create(
            cliente=cliente_obj,
            numero_processo=n_processo,  # <-- NOME EXATO DO SEU MODELO
            status=status_proc,
            descricao="Processo registado através do formulário web." # <-- CAMPO OBRIGATÓRIO PREENCHIDO
        )

        return redirect('consulta')

    return render(request, 'core/cadastro.html')

def consulta(request):
    processos = Processo.objects.all()
    return render(request, 'core/consulta.html', {'processos': processos})