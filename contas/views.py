import calendar
import datetime
import math
from decimal import Decimal

from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import CompraForm, RecebimentoForm, ResponsavelForm, ContaForm
from .models import Responsavel, Conta, Contas_a_pagar, Recebimento


def data(date, format_str='%d/%m/%Y'):
    date_str = date
    return datetime.datetime.strptime(date_str, format_str)


def data_vencimento_str(date, parc, dia_vencimento):
    month = date.month + parc
    year = date.year
    if month > 12:
        year = year + math.floor(month / 12)
        month = month % 12

    return datetime.date(year, month, dia_vencimento)


def gerar_lancamentos_responsaveis_responsavel(request):
    responsaveis = Responsavel.objects.all().order_by('id')

    if not request.GET:
        inicial = datetime.date(datetime.date.today().year, datetime.date.today().month, 1)
        final = datetime.date(datetime.date.today().year, datetime.date.today().month,
                              calendar.monthrange(datetime.date.today().year, datetime.date.today().month)[1])
        responsavel = responsaveis[0].nome
        debitos = Contas_a_pagar.objects.all().filter(responsavel=responsaveis[0].id,
                                                      data_vencimento__range=[inicial, final])
        recebimentos = Recebimento.objects.all().filter(responsavel=responsaveis[0].id,
                                                        data__range=[inicial, final])
    else:
        inicial = data(request.GET.get('data_inicial'), '%Y-%m-%d')
        final = data(request.GET.get('data_final'), '%Y-%m-%d')
        responsavel = Responsavel.objects.all().get(nome=request.GET.get('responsavel_select'))
        debitos = Contas_a_pagar.objects.all().filter(responsavel=responsavel.id,
                                                      data_vencimento__range=[inicial, final])
        recebimentos = Recebimento.objects.all().filter(responsavel=responsavel.id,
                                                        data__range=[inicial, final])

    lancamentos = []
    for debito in debitos:
        parcelas = Contas_a_pagar.objects.all().filter(
            conta=debito.conta.id,
            responsavel=debito.conta.id,
            data_compra=debito.data_compra,
            valor_parcela=debito.valor_parcela
        ).aggregate(parcelas=Count('numero_parcela'))['parcelas']
        if parcelas == 1:
            descricao = 'Dt. {} {}-{}'.format(
                debito.data_compra.strftime('%d/%m/%Y'), debito.conta.nome, debito.descricao
            )
        else:
            descricao = 'Dt. {} {}-{} ({}/{})'.format(
                         debito.data_compra.strftime('%d/%m/%Y'), debito.conta.nome, debito.descricao,
                         debito.numero_parcela, parcelas,
                     )
        lancamentos.append(
            dict(id=debito.id, data=debito.data_vencimento.strftime('%d/%m/%Y'),
                 descricao=descricao, valor=float(debito.valor_parcela) * -1)
        )
    for recebimento in recebimentos:
        lancamentos.append(
            dict(id=recebimento.id, data=recebimento.data.strftime('%d/%m/%Y'), descricao=recebimento.descricao,
                 valor=float(recebimento.valor, )))

    return lancamentos, responsaveis, responsavel, inicial, final


@login_required
def compra_new(request):
    form = CompraForm(request.POST or None)
    contas_a_pagar = Contas_a_pagar.objects.all().order_by('data_compra')
    relatorio = []
    for conta in contas_a_pagar:
        relatorio.append(dict(
            id=conta.id,
            conta=conta.conta,
            responsavel=conta.responsavel,
            data_compra=conta.data_compra.strftime('%d/%m/%Y'),
            descricao=conta.descricao,
            valor_parcela=conta.valor_parcela,
            data_vencimento=conta.data_vencimento.strftime('%d/%m/%Y')
        ))

    if request.POST:
        conta = Conta.objects.all().get(id=request.POST.get('conta'))
        responsavel = Responsavel.objects.all().get(id=request.POST.get('responsavel'))
        valor = float(request.POST.get('valor').replace('.', '').replace(',', '.'))
        quantidade_parcelas = int(request.POST.get('quantidade_parcelas'))
        valor_parcela = valor / quantidade_parcelas
        data_compra = datetime.datetime.strptime(request.POST.get('data_compra'), '%Y-%m-%d')

        if data_compra.day <= conta.dia_fechamento:
            for i in range(quantidade_parcelas):
                data_vencimento = data_vencimento_str(data_compra, i, conta.dia_vencimento)
                Contas_a_pagar.objects.create(
                    conta=conta,
                    responsavel=responsavel,
                    data_compra=data_compra,
                    descricao=request.POST.get('descricao'),
                    numero_parcela=i + 1,
                    valor_parcela=Decimal(valor_parcela),
                    data_vencimento=data_vencimento
                ).save()
        else:
            for i in range(quantidade_parcelas):
                data_vencimento = data_vencimento_str(data_compra, i + 1, conta.dia_vencimento)
                Contas_a_pagar.objects.create(
                    conta=conta,
                    responsavel=responsavel,
                    data_compra=data_compra,
                    descricao=request.POST.get('descricao'),
                    numero_parcela=i + 1,
                    valor_parcela=Decimal(valor_parcela),
                    data_vencimento=data_vencimento
                ).save()
        return redirect('compra_new')

    return render(request, 'new_compra.html', {'form': form, 'relatorio': relatorio})


@login_required
def delete_compra(request, id):
    item = get_object_or_404(Contas_a_pagar, pk=id)
    item.delete()
    return redirect('compra_new')


@login_required
def recebimento_new(request):
    form = RecebimentoForm(request.POST or None)
    recebimentos = Recebimento.objects.all().order_by('data')
    relatorio = []
    for recebimento in recebimentos:
        relatorio.append(dict(
            id=recebimento.id,
            responsavel=recebimento.responsavel,
            data=recebimento.data.strftime('%d/%m/%Y'),
            descricao=recebimento.descricao,
            valor=recebimento.valor,
        ))

    if request.POST:
        responsavel = Responsavel.objects.all().get(id=request.POST.get('responsavel'))
        Recebimento.objects.create(
            responsavel=responsavel,
            data=datetime.datetime.strptime(request.POST.get('data'), '%Y-%m-%d'),
            descricao=request.POST.get('descricao'),
            valor=float(request.POST.get('valor').replace('.', '').replace(',', '.'))
        ).save()
        return redirect('recebimento_new')

    return render(request, 'new_recebimento.html', {'form': form, 'relatorio': relatorio})


@login_required
def delete_recebimento(request, id):
    item = get_object_or_404(Recebimento, pk=id)
    item.delete()
    return redirect('recebimento_new')


@login_required
def responsavel_new(request):
    form = ResponsavelForm(request.POST or None)
    relatorio = Responsavel.objects.all().order_by('id')
    button = 'Salvar'

    if form.is_valid():
        form.save()
        return redirect('responsavel_new')

    return render(request, 'new_responsavel.html', {'form': form, 'relatorio': relatorio, 'nome_botao': button})


@login_required
def responsavel_update(request, id):
    responsavel = get_object_or_404(Responsavel, pk=id)
    form = ResponsavelForm(request.POST or None, request.FILES or None, instance=responsavel)
    relatorio = Responsavel.objects.all().order_by('id')
    button = 'Alterar'

    if form.is_valid():
        form.save()
        return redirect('responsavel_new')

    return render(request, 'new_responsavel.html', {'form': form, 'relatorio': relatorio, 'nome_botao': button})


@login_required
def delete_responsavel(request, id):
    item = get_object_or_404(Responsavel, pk=id)
    item.delete()
    return redirect('responsavel_new')


@login_required
def conta_new(request):
    form = ContaForm(request.POST or None)
    relatorio = Conta.objects.all().order_by('id')
    button = 'Salvar'

    if form.is_valid():
        form.save()
        return redirect('conta_new')

    return render(request, 'new_conta.html', {'form': form, 'relatorio': relatorio, 'nome_botao': button})


@login_required
def conta_update(request, id):
    conta = get_object_or_404(Conta, pk=id)
    form = ContaForm(request.POST or None, request.FILES or None, instance=conta)
    relatorio = Conta.objects.all().order_by('id')
    button = 'Alterar'

    if form.is_valid():
        form.save()
        return redirect('conta_new')

    return render(request, 'new_conta.html', {'form': form, 'relatorio': relatorio, 'nome_botao': button})


@login_required
def delete_conta(request, id):
    item = get_object_or_404(Conta, pk=id)
    item.delete()
    return redirect('conta_new')
