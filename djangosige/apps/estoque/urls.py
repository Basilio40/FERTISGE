# -*- coding: utf-8 -*-

from django.urls import path
from . import views

app_name = 'estoque'
urlpatterns = [
    # Consulta de estoque
    # estoque/consultaestoque/
    path('consultaestoque/', views.ConsultaEstoqueView.as_view(),
        name='consultaestoqueview'),

    # Local de estoque
    # estoque/local/saida/adicionar/
    path('local/saida/adicionar/',
        views.AdicionarLocalEstoqueView.as_view(), name='addlocalview'),
    # estoque/local/listalocal
    path('local/listalocal/', views.LocalEstoqueListView.as_view(),
        name='listalocalview'),
    # estoque/local/editar/
    path('local/editar/<int:pk>/',
        views.EditarLocalEstoqueView.as_view(), name='editarlocalview'),
    # estoque/local/excluir/
    path('local/excluir/<int:pk>/',
        views.ExcluirLocalEstoqueView.as_view(), name='excluirlocalview'),

    # Movimento de estoque
    # Lista todos movimentos
    path('movimentos/', views.MovimentoEstoqueListView.as_view(),
        name='listamovimentoestoqueview'),

    # EntradaEstoque
    # estoque/movimento/adicionarentrada/
    path('movimento/adicionarentrada/',
        views.AdicionarEntradaEstoqueView.as_view(), name='addentradaestoqueview'),
    # estoque/movimento/listaentradas/
    path('movimento/listaentradas/', views.EntradaEstoqueListView.as_view(),
        name='listaentradasestoqueview'),
    # estoque/movimento/editarentrada/
    path('movimento/editarentrada/<int:pk>/', views.DetalharEntradaEstoqueView.as_view(
    ), name='detalharentradaestoqueview'),
    # estoque/movimento/excluirentrada/
    path('movimento/excluirentrada/<int:pk>/',
        views.ExcluirEntradaEstoqueView.as_view(), name='excluirentradaestoqueview'),

    # SaidaEstoque
    # estoque/movimento/adicionarsaida/
    path('movimento/adicionarsaida/',
        views.AdicionarSaidaEstoqueView.as_view(), name='addsaidaestoqueview'),
    # estoque/movimento/listasaidas/
    path('movimento/listasaidas/', views.SaidaEstoqueListView.as_view(),
        name='listasaidasestoqueview'),
    # estoque/movimento/editarsaida/
    path('movimento/editarsaida/<int:pk>/',
        views.DetalharSaidaEstoqueView.as_view(), name='detalharsaidaestoqueview'),
    # estoque/movimento/excluirsaida/
    path('movimento/excluirsaida/<int:pk>/',
        views.ExcluirSaidaEstoqueView.as_view(), name='excluirsaidaestoqueview'),

    # TransferenciaEstoque
    # estoque/movimento/adicionartransferencia/
    path('movimento/adicionartransferencia/',
        views.AdicionarTransferenciaEstoqueView.as_view(), name='addtransferenciaestoqueview'),
    # estoque/movimento/listatransferencias/
    path('movimento/listatransferencias/', views.TransferenciaEstoqueListView.as_view(),
        name='listatransferenciasestoqueview'),
    # estoque/movimento/editartransferencia/
    path('movimento/editartransferencia/<int:pk>/', views.DetalharTransferenciaEstoqueView.as_view(
    ), name='detalhartransferenciaestoqueview'),
]
