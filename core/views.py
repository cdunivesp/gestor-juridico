from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
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

        cliente_obj, created = Cliente.objects.get_or_create(
            cpf=cpf_cliente,
            defaults={
                'nome': nome_cliente,
                'cep': '00000000',
                'endereco': 'Não informado',
                'cidade': 'Não informada'
            }
        )

        novo_processo = Processo.objects.create(
            cliente=cliente_obj,
            numero_processo=n_processo,
            status=status_proc,
            descricao=obs_proc if obs_proc else "Sem observações adicionais."
        )

        if data_proc:
            data_convertida = parse_date(data_proc)
            if data_convertida:
                novo_processo.data_criacao = datetime.combine(data_convertida, datetime.min.time())
                novo_processo.save()

        return redirect('consulta')

    return render(request, 'core/cadastro.html')

def editar(request, id):
    processo = get_object_or_404(Processo, id=id)

    if request.method == 'POST':
        # Atualiza os dados do cliente vinculado
        processo.cliente.nome = request.POST.get('nome')
        processo.cliente.cpf = request.POST.get('cpf')
        processo.cliente.save()

        # Atualiza os dados do processo
        processo.numero_processo = request.POST.get('numero')
        processo.status = request.POST.get('status')
        obs_proc = request.POST.get('observacoes')
        processo.descricao = obs_proc if obs_proc else "Sem observações adicionais."

        data_proc = request.POST.get('data')
        if data_proc:
            data_convertida = parse_date(data_proc)
            if data_convertida:
                processo.data_criacao = datetime.combine(data_convertida, datetime.min.time())

        processo.save()
        return redirect('consulta')

    return render(request, 'core/cadastro.html', {'processo': processo})

def excluir(request, id):
    processo = get_object_or_404(Processo, id=id)
    processo.delete()
    return redirect('consulta')

def consulta(request):
    busca = request.GET.get('busca', '').strip()
    status_filtro = request.GET.get('status', '').strip()

    processos = Processo.objects.all().order_by('-data_criacao')

    if busca:
        processos = processos.filter(
            Q(cliente__nome__icontains=busca) |
            Q(cliente__cpf__icontains=busca) |
            Q(numero_processo__icontains=busca)
        )

    if status_filtro:
        processos = processos.filter(status=status_filtro)

    contexto = {
        'processos': processos,
        'busca': busca,
        'status_filtro': status_filtro,
    }
    return render(request, 'core/consulta.html', contexto)