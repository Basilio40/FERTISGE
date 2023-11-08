from datetime import datetime
from typing import Literal, List

class Endereco: ...

class Contato:
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

class NaturezaOperacao:
    id: int

class FormaPagamento:
    id: int

class Loja:
    id: int
    numero: str

class Items:
    """codigo*	[...]
    descricao	[...]
    unidade	[...]
    quantidade	[...]
    valor	[...]
    tipo	[...]
    pesoBruto	[...]
    pesoLiquido	[...]
    numeroPedidoCompra	[...]
    classificacaoFiscal	[...]
    cest	[...]
    codigoServico	[...]
    origem	[...]
    informacoesAdicionais"""
    ...

class Parcela:
    data: datetime
    valor: float
    
    observacoes: str
    formaPagamento: FormaPagamento

class Transporte: ...
    
class Intermediador: ...
    
class DocumentoReferenciado: ...

class ProdutorRuralReferenciada: ...

class NotaFiscalEletronica:
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
    
    def toJson(self): ...
