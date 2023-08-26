from rolepermissions.roles import AbstractUserRole

class Escritorio(AbstractUserRole):
    available_permissions = {
        'ver_cadastro': True,
        'ver_compras': True,
        'ver_estoque': True,
        'ver_vendas': True,
        'ver_fiscal': True,
    }

class Vend(AbstractUserRole):
    available_permissions = {
        'ver_cadastro': True,
        'ver_vendas': True,
        'ver_estoque': True,
        
    }