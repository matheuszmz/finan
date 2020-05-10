from django import forms
from datetime import date
from .models import Responsavel, Conta, Recebimento


class DateInput(forms.DateInput):
    input_type = 'date'


class CompraForm(forms.Form):
    conta = forms.ModelChoiceField(queryset=Conta.objects.all(), empty_label=None, label='')
    responsavel = forms.ModelChoiceField(queryset=Responsavel.objects.all(), empty_label=None, label='Responśavel pelo Lançamento')
    data_compra = forms.DateField(initial=date.today().strftime('%Y-%m-%d'), widget=DateInput(), label='Data da Compra')
    descricao = forms.CharField(max_length=30, label='Descrição')
    valor = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput, label='Valor R$')
    quantidade_parcelas = forms.IntegerField(widget=forms.TextInput, initial=1, label='Quantidade de Parcelas')


class RecebimentoForm(forms.Form):
    responsavel = forms.ModelChoiceField(queryset=Responsavel.objects.all(), empty_label=None, label="Responsável")
    data = forms.DateField(initial=date.today().strftime('%Y-%m-%d'), widget=DateInput(), label="Data de Recebimento")
    descricao = forms.CharField(max_length=30, label="Descrição")
    valor = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput, label="Valor R$")


class ContaForm(forms.ModelForm):
    class Meta:
        model = Conta
        fields = ['nome', 'dia_fechamento', 'dia_vencimento']


class ResponsavelForm(forms.ModelForm):
    class Meta:
        model = Responsavel
        fields = ['nome']
