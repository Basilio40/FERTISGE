# -*- coding: utf-8 -*-

from django import forms
# from django.utils.translation import ugettext_lazy as _

from djangosige.apps.fiscal.models import NaturezaOperacao


class NaturezaOperacaoForm(forms.ModelForm):

    class Meta:
        model = NaturezaOperacao
        fields = ('cfop', 'descricao', 'tp_operacao', 'id_dest',)
        widgets = {
            'cfop': forms.TextInput(attrs={'class': 'form-control', 'size': '40'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'tp_operacao': forms.Select(attrs={'class': 'form-control'}),
            'id_dest': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'cfop': ('CFOP'),
            'descricao': ('Descrição'),
            'tp_operacao': ('Tipo de operação'),
            'id_dest': ('Local destino da operação'),
        }
