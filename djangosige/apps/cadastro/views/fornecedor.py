# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse

from django.urls import reverse_lazy

from djangosige.apps.cadastro.forms import FornecedorForm
from djangosige.apps.cadastro.models import Fornecedor

from .base import AdicionarPessoaView, PessoasListView, EditarPessoaView


class AdicionarFornecedorView(AdicionarPessoaView):
    template_name = "cadastro/pessoa_add.html"
    success_url = reverse_lazy('cadastro:listafornecedoresview')
    success_message = "Fornecedor <b>%(nome_razao_social)s </b>adicionado com sucesso."
    permission_codename = 'add_fornecedor'

    def get_context_data(self, **kwargs):
        context = super(AdicionarFornecedorView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'CADASTRAR FORNECEDOR'
        context['return_url'] = reverse_lazy('cadastro:listafornecedoresview')
        context['tipo_pessoa'] = 'fornecedor'
        return context

    def get(self, request, *args, **kwargs):
        form = FornecedorForm(prefix='fornecedor_form')
        return super(AdicionarFornecedorView, self).get(request, form, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = FornecedorForm(request.POST, request.FILES,
                              prefix='fornecedor_form', request=request)
        return super(AdicionarFornecedorView, self).post(request, form, *args, **kwargs)


class FornecedoresListView(PessoasListView):
    template_name = 'cadastro/pessoa_list.html'
    model = Fornecedor
    context_object_name = 'all_fornecedores'
    success_url = reverse_lazy('cadastro:listafornecedoresview')
    permission_codename = 'view_fornecedor'

    def get_context_data(self, **kwargs):
        context = super(FornecedoresListView, self).get_context_data(**kwargs)
        context['title_complete'] = 'FORNECEDORES CADASTRADOS'
        context['add_url'] = reverse_lazy('cadastro:addfornecedorview')
        context['tipo_pessoa'] = 'fornecedor'

        for fornecedor in context['all_fornecedores']:
            if fornecedor.tipo_pessoa == 'PF':
                fornecedor.cpf_cnpj = fornecedor.pessoa_fis_info.cpf
            elif fornecedor.tipo_pessoa == 'PJ':
                fornecedor.cpf_cnpj = fornecedor.pessoa_jur_info.cnpj
            else:
                fornecedor.cpf_cnpj = None

        return context


class EditarFornecedorView(EditarPessoaView):
    form_class = FornecedorForm
    model = Fornecedor
    template_name = "cadastro/pessoa_edit.html"
    success_url = reverse_lazy('cadastro:listafornecedoresview')
    success_message = "Fornecedor <b>%(nome_razao_social)s </b>editado com sucesso."
    permission_codename = 'change_fornecedor'

    def get_context_data(self, **kwargs):
        context = super(EditarFornecedorView, self).get_context_data(**kwargs)
        context['return_url'] = reverse_lazy('cadastro:listafornecedoresview')
        context['tipo_pessoa'] = 'fornecedor'
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form_class.prefix = "fornecedor_form"
        form = self.get_form(form_class)

        return super(EditarFornecedorView, self).get(request, form, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = form_class(request.POST, request.FILES,
                          prefix='fornecedor_form', instance=self.object, request=request)
        return super(EditarFornecedorView, self).post(request, form, *args, **kwargs)


class ExcluirFornecedorView(EditarPessoaView):
    def get(self, request, pk):
        cliente = get_object_or_404(Fornecedor, pk=pk)
        cliente.delete()
        success_url = reverse_lazy('cadastro:listafornecedoresview') 
        return redirect('cadastro:listafornecedoresview')