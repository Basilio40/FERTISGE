# -*- coding: utf-8 -*-

import os, sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(".."))

from djangosige.PySIGNFe.pysignfe.nf_e import nf_e

#from djangosige.PySIGNFe.pysignfe.nfe.manual_500.nfe_310 import NFe as NFe_310
from djangosige.PySIGNFe.pysignfe.nfe.manual_600.nfe_310 import NFe as NFe_310
#from djangosige.PySIGNFe.pysignfe.nfe.manual_500.nfe_310 import Det as Det_310
from djangosige.PySIGNFe.pysignfe.nfe.manual_600.nfe_310 import Det as Det_310
from djangosige.PySIGNFe.pysignfe.nfe.webservices_flags import UF_CODIGO

if __name__ == '__main__':
    nova_nfe = nf_e()
    
    #Associacao.pfx nao e valido, utilize um certificado valido
    caminho_certificado = "certificado/Associacao.pfx"
    with open(caminho_certificado, 'rb') as f:
        arquivo = f.read()
    
    info_certificado = nova_nfe.extrair_certificado_a1(arquivo, "associacao")
    
    ##Montar nota fiscal
    
    nfe = NFe_310()
    
    ##Identificação da nota
    
    #nfe.infNFe.ide.cUF.valor       = UF_CODIGO['MG']           #Preenchido automaticamente 
    nfe.infNFe.ide.natOp.valor      = 'Venda de produto'
    nfe.infNFe.ide.indPag.valor     = 2
    #nfe.infNFe.ide.mod.valor       = '55'                      #Preenchido automaticamente
    nfe.infNFe.ide.serie.valor      = 101
    nfe.infNFe.ide.nNF.valor        = 41
    nfe.infNFe.ide.dhEmi.valor      = datetime.now()
    nfe.infNFe.ide.dhSaiEnt.valor   = datetime.now()
    nfe.infNFe.ide.tpNF.valor       = 1                         #0-entrada 1-saida
    nfe.infNFe.ide.idDest.valor     = 1
    nfe.infNFe.ide.cMunFG.valor     = '3106200'
    nfe.infNFe.ide.tpImp.valor      = 1
    #nfe.infNFe.ide.tpEmis.valor    = 1                         #Preenchido automaticamente 
    #nfe.infNFe.ide.tpAmb.valor     = 2                         #Preenchido automaticamente 
    nfe.infNFe.ide.finNFe.valor     = 1
    nfe.infNFe.ide.indFinal.valor  = 0
    nfe.infNFe.ide.indPres.valor    = '1'
    nfe.infNFe.ide.procEmi.valor    = 0            
    #nfe.infNFe.ide.verProc.valor   = 'PySIGNFe'                #Preenchido automaticamente
    
    ##Contingencia
    #nfe.infNFe.ide.dhCont.valor    = datetime.utcnow()
    #nfe.infNFe.ide.xJust.valor     = 'Falha no webservice do Sefaz'
    
    #Identificação do emitente
    nfe.infNFe.emit.CNPJ.valor              = '11111111111111'
    #nfe.infNFe.emit.CPF.valor              = '11111111111111'
    nfe.infNFe.emit.xNome.valor             = 'RAZAO SOCIAL'        
    nfe.infNFe.emit.xFant.valor             = 'Nome Fantasia'
    nfe.infNFe.emit.CRT.valor               = '1'                   #SIMPLES NACIONAL
    nfe.infNFe.emit.IE.valor                = '1111111111111'
    #nfe.infNFe.emit.IM.valor                = '111111111111111'
    #nfe.infNFe.emit.IEST.valor
    
    #Endereco emitente
    nfe.infNFe.emit.enderEmit.xLgr.valor    = 'LOGRADOURO (RUA, PRACA, AVENIDA)'
    nfe.infNFe.emit.enderEmit.nro.valor     = '140'
    nfe.infNFe.emit.enderEmit.xCpl.valor    = ''                        
    nfe.infNFe.emit.enderEmit.xBairro.valor = 'PILAR'
    nfe.infNFe.emit.enderEmit.cMun.valor    = '3106200'
    nfe.infNFe.emit.enderEmit.xMun.valor    = 'BELO HORIONTE'
    nfe.infNFe.emit.enderEmit.UF.valor      = 'MG'
    nfe.infNFe.emit.enderEmit.CEP.valor     = '30390350'
    nfe.infNFe.emit.enderEmit.fone.valor    = '3133333333'
    nfe.infNFe.emit.enderEmit.cPais.valor   = 1058 
    nfe.infNFe.emit.enderEmit.xPais.valor   = 'BRASIL'
    
    
    #Identificação do destinatario
    nfe.infNFe.dest.CNPJ.valor  = '99999999000191'                                                 #Para homologacao
    nfe.infNFe.dest.xNome.valor = 'NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL'     #Para homologacao
    #Endereco destinatario
    nfe.infNFe.dest.enderDest.xLgr.valor    = 'RUA DOIS'
    nfe.infNFe.dest.enderDest.nro.valor     = '140'
    nfe.infNFe.dest.enderDest.xCpl.valor    = ''
    nfe.infNFe.dest.enderDest.xBairro.valor = 'BARRO PRETO'
    nfe.infNFe.dest.enderDest.cMun.valor    = '3106200'
    nfe.infNFe.dest.enderDest.xMun.valor    = 'BELO HORIZONTE'
    nfe.infNFe.dest.enderDest.UF.valor      = 'MG'
    nfe.infNFe.dest.enderDest.CEP.valor     = '30190110'
    nfe.infNFe.dest.enderDest.cPais.valor   = '1058'
    nfe.infNFe.dest.enderDest.xPais.valor   = 'Brasil'
    nfe.infNFe.dest.enderDest.fone.valor    = '3122222222'
    
    #nfe.infNFe.dest.IE.valor = '111111111111'
    nfe.infNFe.dest.indIEDest.valor = '2'
    
    #Detalhamento dos produtos e servicos
    det = Det_310()
    
    det.nItem.valor = 1
    det.prod.cProd.valor    = 'CODIGO DO PRODUTO'
    det.prod.cEAN.valor     = ''
    det.prod.xProd.valor    = 'DESCRIÇÃO DO PRODUTO USADO PARA EMISSÃO'
    det.prod.NCM.valor      = '01012100'
    det.prod.EXTIPI.valor   = ''
    det.prod.genero.valor   = ''
    det.prod.CFOP.valor     = '5101'
    det.prod.uCom.valor     = 'UN'
    det.prod.qCom.valor     = '100.00'
    det.prod.vUnCom.valor   = '10.0000'
    det.prod.vProd.valor    = '1000.00'
    det.prod.cEANTrib.valor = ''
    det.prod.uTrib.valor    = det.prod.uCom.valor
    det.prod.qTrib.valor    = det.prod.qCom.valor
    det.prod.vUnTrib.valor  = det.prod.vUnCom.valor
    det.prod.vFrete.valor   = '0.00'
    det.prod.vSeg.valor     = '0.00'
    det.prod.vDesc.valor    = '0.00'
    det.prod.vOutro.valor   = '0.00'
    
    #Impostos
    det.imposto.ICMS.regime_tributario = 1      #REGIME TRIBUTARIO: SIMPLES NACIONAL
    det.imposto.ICMS.CSOSN.valor    = '400'     #CODIGO DE REGIME APENAS PARA O SIMPLES NACIONAL
    det.imposto.IPI.CST.valor       = '99'
    det.imposto.PIS.CST.valor       = '99'
    det.imposto.COFINS.CST.valor    = '99'
    
    # Os primeiros 188 caracteres desta string
    # são todos os caracteres válidos em tags da NF-e
    #Informacoes adicionais
    det.infAdProd.valor = u'!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ·¸¹º»¼½¾¿À'
    
    #Incluir detalhes na nfe
    nfe.infNFe.det.append(det)
    
    #Totais
    nfe.infNFe.total.ICMSTot.vBC.valor     = '0.00'
    nfe.infNFe.total.ICMSTot.vICMS.valor   = '0.00'
    nfe.infNFe.total.ICMSTot.vBCST.valor   = '0.00'
    nfe.infNFe.total.ICMSTot.vST.valor     = '0.00'
    nfe.infNFe.total.ICMSTot.vProd.valor   = '1000.00'
    nfe.infNFe.total.ICMSTot.vFrete.valor  = '0.00'
    nfe.infNFe.total.ICMSTot.vSeg.valor    = '0.00'
    nfe.infNFe.total.ICMSTot.vDesc.valor   = '0.00'
    nfe.infNFe.total.ICMSTot.vII.valor     = '0.00'
    nfe.infNFe.total.ICMSTot.vIPI.valor    = '0.00'
    nfe.infNFe.total.ICMSTot.vPIS.valor    = '0.00'
    nfe.infNFe.total.ICMSTot.vCOFINS.valor = '0.00'
    nfe.infNFe.total.ICMSTot.vOutro.valor  = '0.00'
    nfe.infNFe.total.ICMSTot.vNF.valor     = '1000.00'
    nfe.infNFe.total.ICMSTot.vICMSDeson.valor = '0.00'
    
    nfe.gera_nova_chave()
    
    #Gera e emite nota fiscal
    processos = nova_nfe.processar_nota(xml_nfe=nfe.xml, cert=info_certificado['cert'], key=info_certificado['key'], versao=u'3.10', ambiente=2, estado=u'MG', contingencia=False, consumidor=False, consultar_servico=False)
    
    print('Status do Lote: ', processos['lote'].resposta.cStat.valor)
    print('Motivo do Lote: ', processos['lote'].resposta.xMotivo.valor)    
        
    ##Status por nota
    for proc in processos['notas']:
        print('NF-e: ', proc.NFe.chave)
        print('\tStatus da nota: ', proc.protNFe.infProt.cStat.valor)
        print('\tNumero do protocolo: ', proc.protNFe.infProt.nProt.valor)
        print('\tMotivo: ', proc.protNFe.infProt.xMotivo.valor)
        
        ##Gerar DANFE/DANFCE
        if proc.protNFe.infProt.nProt.valor:
            if proc.NFe.infNFe.ide.mod == 65:
                nova_nfe.gerar_danfce(proc_nfce=proc.xml, salvar_arquivo=True)
            elif proc.NFe.infNFe.ide.mod == 55:
                nova_nfe.gerar_danfe(proc_nfe=proc.xml, salvar_arquivo=True)
    