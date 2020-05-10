from django.urls import path
from .views import compra_new, extrato_contas, recebimento_new, delete_compra, delete_recebimento, responsavel_new, delete_responsavel, conta_new, delete_conta


urlpatterns = [
    path('', extrato_contas, name='extrato_contas'),
    path('compra/', compra_new, name='compra_new'),
    path('recebimento/', recebimento_new, name='recebimento_new'),
    path('deleteCompra/<int:id>/', delete_compra, name='delete_compra'),
    path('deleteRecebimento/<int:id>/', delete_recebimento, name='delete_recebimento'),
    path('responsavel/', responsavel_new, name='responsavel_new'),
    path('deleteResponsavel/<int:id>/', delete_responsavel, name='delete_responsavel'),
    path('conta/', conta_new, name='conta_new'),
    path('deleteConta/<int:id>/', delete_conta, name='delete_conta'),
]