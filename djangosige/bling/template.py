"""
Tipo de origem Item
    0 Nacional, exceto as indicadas nos códigos 3, 4, 5 e 8
    1 Estrangeira - Importação direta, exceto a indicada no código 6; 2: Estrangeira - Adquirida no mercado interno, exceto a indicada no código 7
    3 Nacional, mercadoria ou bem com Conteúdo de Importação superior a 40% e inferior ou igual a 70%
    4 Nacional, cuja produção tenha sido feita em conformidade com os processos produtivos básicos de que tratam as legislações citadas nos Ajustes
    5 Nacional, mercadoria ou bem com Conteúdo de Importação inferior ou igual a 40%
    6 Estrangeira - Importação direta, sem similar nacional, constante em lista da CAMEX
    7 Estrangeira - Adquirida no mercado interno, sem similar nacional, constante em lista da CAMEX
    8: Nacional, mercadoria ou bem com Conteúdo de Importação superior a 70%
    
Tipo de fretes
    0 Contratação do Frete por conta do Remetente (CIF)
    1 Contratação do Frete por conta do Destinatário (FOB)
    2 Contratação do Frete por conta de Terceiros
    3 Transporte Próprio por conta do Remetente
    4 Transporte Próprio por conta do Destinatário
    9 Sem Ocorrência de Transporte
"""

from decimal import Decimal
from typing import Literal, List
from datetime import datetime, date

class template:
    
    def toJson(self):
        json = {}
        
        for key, item in self.__dict__.items():
            if(key == "numeroDocumento"):
                import ipdb;ipdb.set_trace()
                
            if(not item):
                continue
            
            if(key.startswith("__") or str(item) == "<class 'function'>"):
                continue
            
            elif(issubclass(type(item), template)):
                json.update({key: item.toJson()})
                
            elif(isinstance(item, (list, tuple, set))):
                json.update({key: [subitem.toJson() for subitem in item]})
            
            elif(isinstance(item, (datetime, date))):
                json.update({key: item.strftime("%Y-%m-%d %H-%M-%S")})
                            
            elif(isinstance(item, Decimal)):
                json.update({key: type(self).__annotations__[key](item)})
                
            else: json.update({key: item})

        return json
            

class DocumentoReferenciado: ...

class ProdutorRuralReferenciada: ...

class Intermediador(template):
    # Obrigatório
    numero: str
    serie: str
    data: datetime
    
    def __init__(self, numero: str, serie: str, data: datetime) -> None:
        self.numero = numero
        self.serie = serie
        self.data = data


class Endereco(template):
    # Obrigatorio
    endereco: str
    bairro: str
    municipio: str
    
    # Opicional
    numero: str
    complemento: str
    cep: str
    uf: str
    pais: str
    
    def __init__(self, endereco:str, bairro:str, municipio:str) -> None:
        self.endereco = endereco
        self.bairro = bairro
        self.municipio = municipio


class Contato(template):
    # Obrigatorio
    nome: str
    tipoPessoa: Literal["F", "J", "E"] #Física, jurídica ou estrangeira
    numeroDocumento: str #CPF ou CNPJ apenas números
        
    # Opicional
    ie: str
    rg: str
    contribuinte: Literal[1, 2, 9] #1 - Contribuinte, 2 - Contr insento ICMS, 3 - Non contr
    telefone: str
    email: str
    endereco: Endereco
    
    def __init__(self, nome:str, tipoPessoa: Literal["F", "J", "E"], numeroDocumento: str) -> None:
        self.nome = nome
        self.tipoPessoa = tipoPessoa
        self.numeroDocumento = numeroDocumento


class Loja(template):
    id: int
    numero: str


class Items(template):
    codigo: str
    
    descricao: str
    unidade: str
    quantidade: float
    valor: float
    tipo: Literal["P", "S"] #Produto ou Serviço
    pesoBruto: float
    pesoLiquido: float
    numeroPedidoCompra: str
    classificacaoFiscal: str
    cest: str
    codigoServico: str
    origem: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8]
    informacoesAdicionais: str

    def __init__(self, codigo: str) -> None:
        self.codigo = codigo

class Parcela(template):
    
    class FormaPagamento(template):
        id: int
        
    data: datetime
    valor: float
    
    observacoes: str
    formaPagamento: FormaPagamento


class Transporte(template):
    
    class Veiculo(template):
        placa: str
        uf: str
        marca: str
    
    class Transportador(template):
        # Obrigatório
        nome: str
        
        # Opicional
        numeroDocumento: str
        ie: str
        endereco: Endereco
        
        def __init__(self, nome: str) -> None:
            self.nome = nome
            
    class Volume(template):
        quantidade: int
        especie: str
        numero: str
        pesoBruto: float
        pesoLiquido: float
    
    class Etiqueta(template):
        nome: str
        endereco: str
        numero: str
        complemento: str
        municipio: str
        uf: str
        cep: str
        bairro: str
        
    fretePorConta: Literal[0, 1, 2, 3, 4, 9]
    frete: float
    veiculo: Veiculo
    transportador: Transportador
    volume: Volume
    etiqueta: Etiqueta
    notaFiscalProdutorRuralReferenciada: ProdutorRuralReferenciada
    intermediador: Intermediador


class NotaFiscalEletronica(template):
    
    class NaturezaOperacao(template):
        id: int
    
    # Obrigatorio
    tipo: Literal[0, 1] # 0 entrada - 1 saida,
    contato: Contato
    
    # Opicional
    numero:	str
    dataOperacao: datetime
    naturezaOperacao: NaturezaOperacao
    loja: Loja
    finalidade:	Literal[1, 2, 3, 4] #1 Normal, 2 Complementar, 3 Ajuste, 4 Devolução
    seguro: float
    despesas: float
    desconto: float
    observacoes: str
    documentoReferenciado: DocumentoReferenciado
    
    itens: List[Items]

    parcelas: List[Parcela]
    transporte: Transporte
    notaFiscalProdutorRuralReferenciada: ProdutorRuralReferenciada
    intermediador:	Intermediador
    
    def __init__(self, tipo: Literal[0, 1], contato: Contato) -> None:
        self.tipo = tipo
        self.contato = contato

    
if __name__ == "__main__":
    nota = NotaFiscalEletronica(
        1,
        Contato(
            "Vic Matos",
            "F",
            "545472103245"
        )
    )
    print(nota.toJson())