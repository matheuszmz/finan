from django.contrib import admin
from .models import Responsavel,Conta, Contas_a_pagar, Recebimento


class Contas_a_pagarAdmin(admin.ModelAdmin):
    list_display = ('conta', 'responsavel', 'data_compra', 'descricao', 'valor_parcela',
                    'data_vencimento')
    search_fields = ('conta', 'responsavel', 'data_compra', 'descricao', 'valor_parcela',
                    'data_vencimento')
    list_filter = ('conta', 'responsavel', 'data_compra', 'data_vencimento')


# Register your models here.
admin.site.register(Responsavel)
admin.site.register(Conta)
admin.site.register(Contas_a_pagar, Contas_a_pagarAdmin)
admin.site.register(Recebimento)
