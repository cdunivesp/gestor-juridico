from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=150, verbose_name="Nome Completo")
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    cep = models.CharField(max_length=9, verbose_name="CEP")
    endereco = models.CharField(max_length=250, verbose_name="Endereço")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")

    def __str__(self):
        return self.nome

class Processo(models.Model):
    STATUS_CHOICES = [
        ('Ativo', 'Ativo'),
        ('Suspenso', 'Suspenso'),
        ('Encerrado', 'Encerrado'),
    ]
    
    numero_processo = models.CharField(max_length=30, unique=True, verbose_name="Número do Processo")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Ativo', verbose_name="Status")
    descricao = models.TextField(verbose_name="Descrição / Assunto")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Abertura")

    def __str__(self):
        return f"Processo {self.numero_processo} - {self.cliente.nome}"