# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy

from djangosige.apps.cadastro.forms import ClienteForm
from djangosige.apps.cadastro.models import Cliente
from django.urls import reverse_lazy

from .base import AdicionarPessoaView, PessoasListView, EditarPessoaView


class AdicionarClienteView(AdicionarPessoaView):
    template_name = "cadastro/pessoa_add.html"
    success_url = reverse_lazy('cadastro:listaclientesview')
    success_message = "Cliente <b>%(nome_razao_social)s </b>adicionado com sucesso."
    permission_codename = 'add_cliente'

    def get_context_data(self, **kwargs):
        context = super(AdicionarClienteView, self).get_context_data(**kwargs)
        context['title_complete'] = 'CADASTRAR CLIENTE'
        context['return_url'] = reverse_lazy('cadastro:listaclientesview')
        context['tipo_pessoa'] = 'cliente'
        return context

    def get(self, request, *args, **kwargs):
        form = ClienteForm(prefix='cliente_form')
        return super(AdicionarClienteView, self).get(request, form, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        req_post = request.POST.copy()
        req_post['cliente_form-limite_de_credito'] = req_post['cliente_form-limite_de_credito'].replace(
            '.', '')
        request.POST = req_post
        form = ClienteForm(request.POST, request.FILES,
                           prefix='cliente_form', request=request)
        return super(AdicionarClienteView, self).post(request, form, *args, **kwargs)


class ClientesListView(PessoasListView):
    template_name = 'cadastro/pessoa_list.html'
    model = Cliente
    context_object_name = 'all_clientes'
    success_url = reverse_lazy('cadastro:listaclientesview')
    permission_codename = 'view_cliente'

    def get_context_data(self, **kwargs):
        context = super(ClientesListView, self).get_context_data(**kwargs)
        context['title_complete'] = 'CLIENTES CADASTRADOS'
        context['add_url'] = reverse_lazy('cadastro:addclienteview')
        context['tipo_pessoa'] = 'cliente'

        for cliente in context['all_clientes']:
            if cliente.tipo_pessoa == 'PF':
                cliente.cpf_cnpj = cliente.pessoa_fis_info.cpf
            elif cliente.tipo_pessoa == 'PJ':
                cliente.cpf_cnpj = cliente.pessoa_jur_info.cnpj
            else:
                cliente.cpf_cnpj = None

        return context

class EditarClienteView(EditarPessoaView):
    form_class = ClienteForm
    model = Cliente
    template_name = "cadastro/pessoa_edit.html"
    success_url = reverse_lazy('cadastro:listaclientesview')
    success_message = "Cliente <b>%(nome_razao_social)s </b>editado com sucesso."
    permission_codename = 'change_cliente'

    def get_context_data(self, **kwargs):
        context = super(EditarClienteView, self).get_context_data(**kwargs)
        context['return_url'] = reverse_lazy('cadastro:listaclientesview')
        context['tipo_pessoa'] = 'cliente'
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form_class.prefix = "cliente_form"
        form = self.get_form(form_class)

        return super(EditarClienteView, self).get(request, form, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        req_post = request.POST.copy()
        req_post['cliente_form-limite_de_credito'] = req_post['cliente_form-limite_de_credito'].replace(
            '.', '')
        request.POST = req_post
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = form_class(request.POST, request.FILES,
                          prefix='cliente_form', instance=self.object, request=request)
        return super(EditarClienteView, self).post(request, form, *args, **kwargs)

class ExcluirClienteView(EditarPessoaView):
    def get(self, request, pk):
        cliente = get_object_or_404(Cliente, pk=pk)
        cliente.delete()
        success_url = reverse_lazy('cadastro:listaclientesview') 
        return redirect('cadastro:listaclientesview')