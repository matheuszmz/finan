from django.db import models


class Responsavel(models.Model):
    nome = models.CharField(max_length=30)

    def __str__(self):
        return self.nome


class Conta(models.Model):
    nome = models.CharField(max_length=30)
    dia_fechamento = models.IntegerField()
    dia_vencimento = models.IntegerField()

    def __str__(self):
        return self.nome


class Contas_a_pagar(models.Model):
    conta = models.ForeignKey(Conta, on_delete=models.PROTECT)
    responsavel = models.ForeignKey(Responsavel, on_delete=models.PROTECT)
    data_compra = models.DateField()
    descricao = models.CharField(max_length=30)
    numero_parcela = models.IntegerField()
    valor_parcela = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()

    def __str__(self):
        return '{} - vencimento: {} : R$ {} '.format(self.numero_parcela, self.data_vencimento, self.valor_parcela)


class Recebimento(models.Model):
    responsavel = models.ForeignKey(Responsavel, on_delete=models.PROTECT)
    data = models.DateField()
    descricao = models.CharField(max_length=30)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return 'Data: {}  {}  R$ {}'.format(self.data, self.descricao, self.valor)
