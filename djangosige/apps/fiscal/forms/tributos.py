# -*- coding: utf-8 -*-

from django import forms
# from django.utils.translation import ugettext_lazy as _
from djangosige.apps.fiscal.models import GrupoFiscal, ICMS, ICMSSN, ICMSUFDest, IPI, PIS, COFINS


class GrupoFiscalForm(forms.ModelForm):

    class Meta:
        model = GrupoFiscal
        fields = ('descricao', 'regime_trib',)
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'title': 'Insira uma breve descrição do grupo fiscal, EX: ICMS (Simples Nacional) + IPI'}),
            'regime_trib': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'descricao': ('Descrição'),
            'regime_trib': ('Regime Tributário'),
        }


class ICMSForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        if 'grupo_fiscal' in kwargs:
            grupo_fiscal = kwargs.pop('grupo_fiscal')
            instance = ICMS.objects.get(grupo_fiscal=grupo_fiscal)
            super(ICMSForm, self).__init__(instance=instance, *args, **kwargs)
        else:
            super(ICMSForm, self).__init__(*args, **kwargs)

        self.fields['cst'].required = False

        self.fields['p_icms'].localize = True
        self.fields['p_red_bc'].localize = True
        self.fields['p_mvast'].localize = True
        self.fields['p_red_bcst'].localize = True
        self.fields['p_icmsst'].localize = True
        self.fields['p_dif'].localize = True
        self.fields['p_bc_op'].localize = True

    class Meta:
        model = ICMS
        fields = ('cst', 'mod_bc', 'p_icms', 'p_red_bc', 'mod_bcst', 'p_mvast', 'p_red_bcst', 'p_icmsst', 'mot_des_icms',
                  'p_dif', 'p_bc_op', 'ufst', 'icms_incluido_preco', 'icmsst_incluido_preco',
                  'cfop', 'cfop_ufd',)
        
        widgets = {
            'cst': forms.Select(attrs={'class': 'form-control'}),
            'mod_bc': forms.Select(attrs={'class': 'form-control'}),
            'p_icms': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'p_red_bc': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'mod_bcst': forms.Select(attrs={'class': 'form-control'}),
            'p_mvast': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'p_red_bcst': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'p_icmsst': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'mot_des_icms': forms.Select(attrs={'class': 'form-control'}),
            'p_dif': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'p_bc_op': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'ufst': forms.Select(attrs={'class': 'form-control'}),
            'icms_incluido_preco': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'icmsst_incluido_preco': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cfop': forms.Select(attrs={'class': 'form-control cfop-select'}),
            'cfop_ufd': forms.Select(attrs={'class': 'form-control cfop-select'}),
        }
        labels = {
            'cst': ('CST ICMS'),
            'mod_bc': ('Modalidade de determinação da BC do ICMS'),
            'p_icms': ('Alíquota ICMS'),
            'p_red_bc': ('% da Redução de BC'),
            'mod_bcst': ('Modalidade de determinação da BC do ICMS ST'),
            'p_mvast': ('% Margem de valor Adicionado do ICMS ST'),
            'p_red_bcst': ('% da Redução de BC do ICMS ST'),
            'p_icmsst': ('Alíquota ICMS ST'),
            'mot_des_icms': ('Motivo da desoneração do ICMS'),
            'p_dif': ('% do diferimento'),
            'p_bc_op': ('% da BC operação própria'),
            'ufst': ('UF para qual é devido o ICMS ST'),
            'icms_incluido_preco': ('ICMS incluso no preço'),
            'icmsst_incluido_preco': ('ICMS-ST incluso no preço'),
            'cfop': ('CFOP Entrada mesma UF'),
            'cfop_ufd': ('CFOP Entrada outra UF'),
        }


class ICMSSNForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        if 'grupo_fiscal' in kwargs:
            grupo_fiscal = kwargs.pop('grupo_fiscal')
            instance = ICMSSN.objects.get(grupo_fiscal=grupo_fiscal)
            super(ICMSSNForm, self).__init__(
                instance=instance, *args, **kwargs)
        else:
            super(ICMSSNForm, self).__init__(*args, **kwargs)

        self.fields['csosn'].required = False

        self.fields['p_cred_sn'].localize = True
        self.fields['p_icms'].localize = True
        self.fields['p_red_bc'].localize = True
        self.fields['p_mvast'].localize = True
        self.fields['p_red_bcst'].localize = True
        self.fields['p_icmsst'].localize = True

    class Meta:
        model = ICMSSN
        fields = ('csosn', 'p_cred_sn', 'p_icms', 'mod_bcst', 'mod_bc', 'p_red_bc', 'p_mvast', 'p_red_bcst', 'p_icmsst',
                  'icmssn_incluido_preco', 'icmssnst_incluido_preco', 'cfop', 'cfop_ufd',)
        widgets = {
            'csosn': forms.Select(attrs={'class': 'form-control'}),
            'p_cred_sn': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'mod_bc': forms.Select(attrs={'class': 'form-control'}),
            'p_icms': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'p_red_bc': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'mod_bcst': forms.Select(attrs={'class': 'form-control'}),
            'p_mvast': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'p_red_bcst': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'p_icmsst': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'icmssn_incluido_preco': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'icmssnst_incluido_preco': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cfop': forms.Select(attrs={'class': 'form-control cfop-select'}),
            'cfop_ufd': forms.Select(attrs={'class': 'form-control cfop-select'}),
        }
        labels = {
            'csosn': ('CSOSN'),
            'p_cred_sn': ('Alíquota aplicável de cálculo do crédito'),
            'mod_bc': ('Modalidade de determinação da BC do ICMS'),
            'p_icms': ('Alíquota ICMS'),
            'p_red_bc': ('% da Redução de BC'),
            'mod_bcst': ('Modalidade de determinação da BC do ICMS ST'),
            'p_mvast': ('% Margem de valor Adicionado do ICMS ST'),
            'p_red_bcst': ('% da Redução de BC do ICMS ST'),
            'p_icmsst': ('Alíquota ICMS ST'),
            'icmssn_incluido_preco': ('ICMS incluso no preço'),
            'icmssnst_incluido_preco': ('ICMS-ST incluso no preço'),
            'cfop': ('CFOP Saida mesma UF'),
            'cfop_ufd': ('CFOP Saida outra UF'),
        }


class ICMSUFDestForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        if 'grupo_fiscal' in kwargs:
            grupo_fiscal = kwargs.pop('grupo_fiscal')
            instance = ICMSUFDest.objects.get(grupo_fiscal=grupo_fiscal)
            super(ICMSUFDestForm, self).__init__(
                instance=instance, *args, **kwargs)
        else:
            super(ICMSUFDestForm, self).__init__(*args, **kwargs)

        self.fields['p_fcp_dest'].localize = True
        self.fields['p_icms_dest'].localize = True
        self.fields['p_icms_inter'].localize = True
        self.fields['p_icms_inter_part'].localize = True

    class Meta:
        model = ICMSUFDest
        fields = ('p_fcp_dest', 'p_icms_dest',
                  'p_icms_inter', 'p_icms_inter_part', )
        widgets = {
            'p_fcp_dest': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'p_icms_dest': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'p_icms_inter': forms.Select(attrs={'class': 'form-control'}),
            'p_icms_inter_part': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'p_fcp_dest': ('% do ICMS relativo ao FCP de destino'),
            'p_icms_dest': ('Alíquota interna da UF de destino'),
            'p_icms_inter': ('Alíquota interestadual das UF envolvidas'),
            'p_icms_inter_part': ('% provisório de partilha do ICMS Interestadual'),
        }


class IPIForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        if 'grupo_fiscal' in kwargs:
            grupo_fiscal = kwargs.pop('grupo_fiscal')
            instance = IPI.objects.get(grupo_fiscal=grupo_fiscal)
            super(IPIForm, self).__init__(instance=instance, *args, **kwargs)
        else:
            super(IPIForm, self).__init__(*args, **kwargs)

        self.fields['p_ipi'].localize = True
        self.fields['valor_fixo'].localize = True

    class Meta:
        model = IPI
        fields = ('cst', 'cl_enq', 'c_enq', 'cnpj_prod', 'tipo_ipi', 'p_ipi',
                  'valor_fixo', 'ipi_incluido_preco', 'incluir_bc_icms', 'incluir_bc_icmsst',)
        widgets = {
            'cst': forms.Select(attrs={'class': 'form-control'}),
            'cl_enq': forms.TextInput(attrs={'class': 'form-control'}),
            'c_enq': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj_prod': forms.TextInput(attrs={'class': 'form-control'}),
            'p_ipi': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'tipo_ipi': forms.Select(attrs={'class': 'form-control'}),
            'valor_fixo': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'ipi_incluido_preco': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'incluir_bc_icms': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'incluir_bc_icmsst': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'cst': ('CST IPI'),
            'cl_enq': ('Classe de enquadramento para Cigarros e Bebidas'),
            'c_enq': ('Código de Enquadramento Legal'),
            'cnpj_prod': ('CNPJ do produtor da mercadoria'),
            'p_ipi': ('Alíquota do IPI'),
            'tipo_ipi': ('Tipo de cáculo'),
            'valor_fixo': ('Vl. fixo IPI (por produto)'),
            'ipi_incluido_preco': ('IPI incluso no preço'),
            'incluir_bc_icms': ('Incluir IPI na BC do ICMS'),
            'incluir_bc_icmsst': ('Incluir IPI na BC do ICMS-ST'),
        }


class PISForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        if 'grupo_fiscal' in kwargs:
            grupo_fiscal = kwargs.pop('grupo_fiscal')
            instance = PIS.objects.get(grupo_fiscal=grupo_fiscal)
            super(PISForm, self).__init__(instance=instance, *args, **kwargs)
        else:
            super(PISForm, self).__init__(*args, **kwargs)

        self.fields['p_pis'].localize = True
        self.fields['valiq_pis'].localize = True

    class Meta:
        model = PIS
        fields = ('cst', 'p_pis', 'valiq_pis',)
        widgets = {
            'cst': forms.Select(attrs={'class': 'form-control'}),
            'p_pis': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'valiq_pis': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
        }
        labels = {
            'cst': ('CST PIS'),
            'p_pis': ('Alíquota do PIS (em %)'),
            'valiq_pis': ('Alíquota do PIS por produto (em R$)'),
        }


class COFINSForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        if 'grupo_fiscal' in kwargs:
            grupo_fiscal = kwargs.pop('grupo_fiscal')
            instance = COFINS.objects.get(grupo_fiscal=grupo_fiscal)
            super(COFINSForm, self).__init__(
                instance=instance, *args, **kwargs)
        else:
            super(COFINSForm, self).__init__(*args, **kwargs)

        self.fields['p_cofins'].localize = True
        self.fields['valiq_cofins'].localize = True

    class Meta:
        model = COFINS
        fields = ('cst', 'p_cofins', 'valiq_cofins',)
        widgets = {
            'cst': forms.Select(attrs={'class': 'form-control'}),
            'p_cofins': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'valiq_cofins': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
        }
        labels = {
            'cst': ('CST COFINS'),
            'p_cofins': ('Alíquota do COFINS (em %)'),
            'valiq_cofins': ('Alíquota do COFINS por produto (em R$)'),
        }
