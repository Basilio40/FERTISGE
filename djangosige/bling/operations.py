from .template import *
from .connection import *

class BlingAPI:
    erro: bool = False 
    
    def montar_nota(self, nota_obj):
        
        # Identificacação do destinatario
        if nota_obj.emit_saida:
            tipo_pessoa = "E" if(nota_obj.dest_saida.id_estrangeiro) else \
                "F" if(nota_obj.dest_saida.tipo_pessoa == 'PF') else \
                "J"

            contato = Contato(
                nota_obj.emit_saida.nome_razao_social, 
                tipo_pessoa,
                nota_obj.emit_saida.cpf_cnpj_apenas_digitos,
            )
            contato.ie = nota_obj.dest_saida.inscricao_estadual
            #contato.contribuinte
            if nota_obj.dest_saida.telefone_padrao:
                contato.telefone = nota_obj.dest_saida.telefone_padrao.get_telefone_apenas_digitos()
            #contato.email
            
            contato.endereco = Endereco(
                nota_obj.dest_saida.endereco_padrao.logradouro,
                nota_obj.dest_saida.endereco_padrao.bairro,
                nota_obj.dest_saida.endereco_padrao.municipio      
            )
            contato.endereco.numero = nota_obj.dest_saida.endereco_padrao.numero
            contato.endereco.complemento = nota_obj.dest_saida.endereco_padrao.complemento
            contato.endereco.cep = nota_obj.dest_saida.endereco_padrao.cep
            contato.endereco.uf = nota_obj.dest_saida.endereco_padrao.uf
            contato.endereco.pais = nota_obj.dest_saida.endereco_padrao.pais
        
        else:
            self.erro = True
            return
        
        nfe = NotaFiscalEletronica(
            nota_obj.tpnf,
            contato)
        nfe.id = nota_obj.id
        #nfe.numero
        nfe.naturezaOperacao = nota_obj.natop
        nfe.finalidade = 1
        
        #nfe.seguro
        #nfe.despesas
        #nfe.desconto
        #nfe.observacoes
        #nfe.documentoReferenciado
        
        nfe.itens = []
        for index, item in enumerate(nota_obj.venda.itens_venda.all(), 1):
            obj = Items(item.produto.codigo)
            obj.descricao = item.produto.descricao
            obj.unidade = item.produto.get_sigla_unidade()
            obj.quantidade = item.quantidade
            obj.valor = item.get_valor_desconto()
            obj.tipo = "P"
            obj.informacoesAdicionais = item.inf_ad_prod
            
            obj.classificacaoFiscal = item.produto.ncm[0:8]
            obj.cest = item.produto.cest
            obj.codigoServico = item.produto.get_cfop_padrao()
            obj.origem = item.produto.origem
            nfe.itens.append(obj)
        
        nfe.parcelas = []
        for pagamento in nota_obj.venda.parcela_pagamento.all():
            parc = Parcela()
            parc.data = pagamento.vencimento
            parc.valor = pagamento.valor_parcela
            nfe.parcelas.append(parc)
        
        nfe.transporte = Transporte()
        if(nota_obj.venda.transportadora):
            ...
        return nfe
    
class BlingNfe(BlingAPI):
    r: RequestBling
    
    def __init__(self) -> None:
        super().__init__()
        
        self.r = RequestBling()
    
    def criar_nota(self, nota:NotaFiscalEletronica):
        return self.r.action("POST", API[NFE]["criar_nota"], data=nota.toJson())
    
    def get_nota_id(self):
        return self.r.action("GET", API[NFE]["nota"])
    
    def enviar_nota(self, id):
        return self.r.action("POST", API[NFE]["enviar_nota"].format(id_nota=id))
    
    def lancar_nota(self, id):
        return self.r.action("POST", API[NFE]["lancar_nota"].format(id_nota=id))
    
    def estornar_nota(self, id):
        return self.r.action("POST", API[NFE]["estornar_nota"].format(id_nota=id))

if (__name__ == "__main__"):
    import ipdb;ipdb.set_trace()
    print("Teste")