# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.http import HttpResponse

from django.contrib.auth.models import User
from djangosige.apps.cadastro.models import Cliente, Fornecedor, Produto, Empresa, Transportadora
from djangosige.apps.vendas.models import OrcamentoVenda, PedidoVenda
from djangosige.apps.compras.models import OrcamentoCompra, PedidoCompra
from djangosige.apps.financeiro.models import MovimentoCaixa, Entrada, Saida
from djangosige.apps.estoque.models import MovimentoEstoque
from rolepermissions.roles import assign_role, get_user_roles
from rolepermissions.permissions import revoke_permission, grant_permission
from rolepermissions.decorators import has_role_decorator , has_permission_decorator

from datetime import datetime

def criar_usuario(request):
    user = User.objects.create_user(username="vendedor",password="1234")
    user.save()
    assign_role(user, 'vend')
    return HttpResponse('Usuario salvo com sucesso')

class IndexView(TemplateView):
    template_name = 'base/index.html'

    def get_fluxo_de_caixa(self):
        data_atual = data_atual = datetime.now().date()
        context = {}
        
        try:
            context['movimento_dia'] = MovimentoCaixa.objects.get(
                data_movimento=data_atual)
        except (MovimentoCaixa.DoesNotExist, ObjectDoesNotExist):
            ultimo_mvmt = MovimentoCaixa.objects.filter(data_movimento__lte=data_atual).latest('data_movimento')
            if ultimo_mvmt:
                context['saldo'] = ultimo_mvmt.saldo_final
            else:
                context['saldo'] = '0,00'

        return context
    

    
    def get_fluxo_de_estoque(self):
        from decimal import Decimal
        
        data_atual = data_atual = datetime.now().date()
        context = {
            "itens_qtd": Decimal(0),
            "valor_entrada": Decimal(0),
            "valor_saida": Decimal(0),
            "valor_total": Decimal(0)
        }
        
        try:
            movimentos = MovimentoEstoque.objects.filter(data_movimento=data_atual)
            if movimentos:
                for mov in movimentos:
                    try:
                        context['valor_entrada'] += mov.entradaestoque.valor_total
                    except: ...
                    
                    try:
                        context['valor_saida'] += mov.saidaestoque.valor_total
                    except: ...
                    
                    context['valor_total'] += mov.valor_total
                    context["itens_qtd"] += mov.quantidade_itens
        
        except (MovimentoEstoque.DoesNotExist, ObjectDoesNotExist): ...
        
        
        context["valor_entrada"] = Entrada.static_format_valor_liquido(context["valor_entrada"])
        context["valor_saida"] = Entrada.static_format_valor_liquido(context["valor_saida"])
        context["valor_total"] = Entrada.static_format_valor_liquido(context["valor_total"])
        return {'estoque_dia': context}
    
    def get_contas_a_pagar(self):
        data_atual = data_atual = datetime.now().date()
        context = {}
        
        try:
            context['contas_pagar'] = Saida.objects.get(data_vencimento=data_atual)
            
        except (Saida.DoesNotExist, ObjectDoesNotExist):
            ...

        return context
    
    def get_contas_a_receber(self):
        data_atual = data_atual = datetime.now().date()
        context = {}
        
        try:
            context['contas_receber'] = Entrada.objects.get(data_vencimento=data_atual)
            
        except (Entrada.DoesNotExist, ObjectDoesNotExist):
            ...

        return context
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        quantidade_cadastro = {}
        agenda_hoje = {}
        alertas = {}
        data_atual = datetime.now().date()

        context['data_atual'] = data_atual.strftime('%d/%m/%Y')

        quantidade_cadastro['clientes'] = Cliente.objects.all().count()
        quantidade_cadastro['fornecedores'] = Fornecedor.objects.all().count()
        quantidade_cadastro['produtos'] = Produto.objects.all().count()
        quantidade_cadastro['empresas'] = Empresa.objects.all().count()
        quantidade_cadastro[
            'transportadoras'] = Transportadora.objects.all().count()
        context['quantidade_cadastro'] = quantidade_cadastro

        agenda_hoje['orcamento_venda_hoje'] = OrcamentoVenda.objects.filter(
            data_vencimento=data_atual, status='0').count()
        agenda_hoje['orcamento_compra_hoje'] = OrcamentoCompra.objects.filter(
            data_vencimento=data_atual, status='0').count()
        agenda_hoje['pedido_venda_hoje'] = PedidoVenda.objects.filter(
            data_entrega=data_atual, status='0').count()
        agenda_hoje['pedido_compra_hoje'] = PedidoCompra.objects.filter(
            data_entrega=data_atual, status='0').count()
        agenda_hoje['contas_receber_hoje'] = Entrada.objects.filter(
            data_vencimento=data_atual, status__in=['1', '2']).count()
        agenda_hoje['contas_pagar_hoje'] = Saida.objects.filter(
            data_vencimento=data_atual, status__in=['1', '2']).count()
        context['agenda_hoje'] = agenda_hoje

        alertas['produtos_baixo_estoque'] = Produto.objects.filter(
            estoque_atual__lte=F('estoque_minimo')).count()
        alertas['orcamentos_venda_vencidos'] = OrcamentoVenda.objects.filter(
            data_vencimento__lte=data_atual, status='0').count()
        alertas['pedidos_venda_atrasados'] = PedidoVenda.objects.filter(
            data_entrega__lte=data_atual, status='0').count()
        alertas['orcamentos_compra_vencidos'] = OrcamentoCompra.objects.filter(
            data_vencimento__lte=data_atual, status='0').count()
        alertas['pedidos_compra_atrasados'] = PedidoCompra.objects.filter(
            data_entrega__lte=data_atual, status='0').count()
        alertas['contas_receber_atrasadas'] = Entrada.objects.filter(
            data_vencimento__lte=data_atual, status__in=['1', '2']).count()
        alertas['contas_pagar_atrasadas'] = Saida.objects.filter(
            data_vencimento__lte=data_atual, status__in=['1', '2']).count()
        context['alertas'] = alertas

        context.update(self.get_fluxo_de_caixa())
        context.update(self.get_contas_a_pagar())
        context.update(self.get_contas_a_receber())
        context.update(self.get_fluxo_de_estoque())
        return context


def handler404(request):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


def handler500(request):
    response = render(request, '500.html', {})
    response.status_code = 500
    return response
