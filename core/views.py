from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date
from datetime import datetime
from .models import Cliente, Processo

def home(request):
    return render(request, 'core/index.html')

def cadastro(request):
    if request.method == 'POST':
        nome_cliente = request.POST.get('nome')
        cpf_cliente = request.POST.get('cpf')
        n_processo = request.POST.get('numero')
        status_proc = request.POST.get('status')
        data_proc = request.POST.get('data')
        obs_proc = request.POST.get('observacoes')

        # 1. Busca ou cria o Cliente pelo CPF
        cliente_obj, created = Cliente.objects.get_or_create(
            cpf=cpf_cliente,
            defaults={
                'nome': nome_cliente,
                'cep': '00000000',
                'endereco': 'Não informado',
                'cidade': 'Não informada'
            }
        )

        # 2. Cria o Processo gravando as observações no campo 'descricao'
        novo_processo = Processo.objects.create(
            cliente=cliente_obj,
            numero_processo=n_processo,
            status=status_proc,
            descricao=obs_proc if obs_proc else "Sem observações adicionais."
        )

        # 3. Se o usuário informou uma data no formulário, atualiza a data do processo
        if data_proc:
            data_convertida = parse_date(data_proc)
            if data_convertida:
                novo_processo.data_criacao = datetime.combine(data_convertida, datetime.min.time())
                novo_processo.save()

        return redirect('consulta')

    return render(request, 'core/cadastro.html')

def consulta(request):
    processos = Processo.objects.all().order_by('-data_criacao')
    return render(request, 'core/consulta.html', {'processos': processos})