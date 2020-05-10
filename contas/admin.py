from django.contrib import admin
from .models import Responsavel,Conta, Contas_a_pagar, Recebimento

# Register your models here.
admin.site.register(Responsavel)
admin.site.register(Conta)
admin.site.register(Contas_a_pagar)
admin.site.register(Recebimento)