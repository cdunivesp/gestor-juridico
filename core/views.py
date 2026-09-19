from django.shortcuts import render, redirect
from .models import Cliente, Processo

def home(request):
    return render(request, 'core/index.html')

def cadastro(request):
    if request.method == 'POST':
        nome_cliente = request.POST.get('nome')
        cpf_cliente = request.POST.get('cpf')  # Captura o novo campo CPF
        numero_processo = request.POST.get('numero')
        status_processo = request.POST.get('status')

        # get_or_create: Procura o cliente pelo CPF. Se não existir, cria um novo.
        cliente_obj, created = Cliente.objects.get_or_create(
            cpf=cpf_cliente,
            defaults={'nome': nome_cliente}
        )

        # Cria o processo e associa-o ao cliente encontrado/criado
        Processo.objects.create(
            cliente=cliente_obj,
            numero=numero_processo,
            status=status_processo
        )

        return redirect('consulta')

    return render(request, 'core/cadastro.html')

def consulta(request):
    processos = Processo.objects.all()
    return render(request, 'core/consulta.html', {'processos': processos})