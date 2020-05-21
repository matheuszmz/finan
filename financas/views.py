from django.contrib.auth import logout
from django.shortcuts import render, redirect

from contas.views import gerar_lancamentos_responsaveis_responsavel


def home(request):
    lancamentos, responsaveis, responsavel, inicial, final = gerar_lancamentos_responsaveis_responsavel(request)

    return render(request, 'index.html', {'relatorio': lancamentos,
                                          'data_inicial': inicial.strftime('%Y-%m-%d'),
                                          'data_final': final.strftime('%Y-%m-%d'),
                                          'responsaveis': responsaveis,
                                          'responsavel_select': responsavel,
                                          'saldo': round(sum([i['valor'] for i in lancamentos]), 2)
                                          })


def my_logout(request):
    logout(request)
    return redirect('index')
