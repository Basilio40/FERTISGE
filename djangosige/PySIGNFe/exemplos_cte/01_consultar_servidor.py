# -*- coding: utf-8 -*-

import os, sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(".."))

from djangosige.PySIGNFe.pysignfe.ct_e import ct_e

if __name__ == '__main__':
    mycte = ct_e()
    
    #Associacao.pfx nao e valido, utilize um certificado valido
    caminho_certificado = "certificado/BRASIL FERTILIZANTES E RECICLAGEM LTDA38226805000120.pfx"
    with open(caminho_certificado, 'rb') as f:
        arquivo = f.read()
    
    info_certificado = mycte.extrair_certificado_a1(arquivo, "1234")
       
    resultado = mycte.consultar_servidor(cert=info_certificado['cert'], key=info_certificado['key'], ambiente=2, versao=u'3.00', estado=u'MT', salvar_arquivos=False)
    print('Status: '+str(resultado['status']))
    print('Razao: '+str(resultado['reason']))