import base64
import random
import string

import json
import requests

from djangosige.apps.cadastro.models import BlingAccount

HOST = 0
AUTH = 1
NFCE = 2
NFSE = 3
NFE = 4
OP = 5

API = {
    HOST : u"https://www.bling.com.br/Api/v3",
    AUTH : {
        u"login": u"/oauth/login?",
        u"token": u"/oauth/token?",
        u"auth": u"/oauth/authorize?"
    },
    NFCE: {
        u"nota": u"/nfce/{id_nota}",
        u"enviar_nota": u"/nfce/{id_nota}/enviar",
        u"lancar_nota": u"/nfce/{id_nota}/lancar-contas",
        u"estornar_nota": u"/nfce/{id_nota}/estornar-contas"
    },
    NFSE: {
        u"nota": u"/nfse/{id_nota}",
        u"enviar_nota": u"/nfse/{id_nota}/enviar",
        u"lancar_nota": u"/nfse/{id_nota}/lancar-contas",
        u"estornar_nota": u"/nfse/{id_nota}/estornar-contas"
    },
    NFE: {
        u"nota": u"/nfe/{id_nota}",
        u"enviar_nota": u"/nfe/{id_nota}/enviar",
        u"lancar_nota": u"/nfe/{id_nota}/lancar-contas",
        u"estornar_nota": u"/nfe/{id_nota}/estornar-contas"
    },
    OP: {
        "naturezas": "/naturezas-operacoes"
    },
}

from datetime import datetime, timedelta

class TokenControl:
    access: str
    refresh: str
    
    validity: datetime
    
    def set(self, response: dict):
        self.access = response["access_token"]
        self.refresh = response["refresh_token"]
        
        self.validity = datetime.now() \
            + timedelta(seconds=int(response["expires_in"]))
    
    def expires(self) -> bool:
        return self.validity <= datetime.now()


class RequestBing:
    credential: BlingAccount
    connection: requests.sessions.Session
    token: TokenControl
    refresh: str
    headers: dict
    state: str
    auth: str
    
    def __init__(self):
        self.credential = BlingAccount.objects.last()
        self.auth = 'Basic {}'.format(
            base64.b64encode((self.credential.api_id + u":" + self.credential.api_secret).encode("ascii"))
            .decode("ascii"))
        
        self.connection = requests.session()
        self.headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "1.0",
            "Authorization": self.auth,
        }
        
        self.state = ''.join(
            random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8)
        )
        self.token = TokenControl()
        self.get_auth()
        return

    def get_auth(self):
        self.headers["Authorization"] = self.auth
        
        payload = {
            "login": self.credential.username,
            "password": self.credential.password,
        }
        
        url = API[HOST] \
            + "{}" \
            + f"client_id={self.credential.api_id}&response_type=code&state={self.state}"
        
        resp = self.connection.get(url=url.format(API[AUTH]["auth"]), headers=self.headers)
        resp = self.connection.post(url=url.format(API[AUTH]["login"]), data=payload, headers=self.headers)

        assert len(resp.history) > 1, "Não foi possível fazer autenticação na API do Bling"
        
        code = resp.history[-1].url.split("code=")[-1].split("&")[0]        
        url = API[HOST] \
            + API[AUTH]["token"]
        
        payload = {
            "grant_type": "authorization_code",
            "code": code
        }
        resp = self.connection.post(url=url, data=payload, headers=self.headers)
        
        assert resp.status_code == 200, "Não foi possível criar token de acesso"
        self.token.set(json.loads(resp.content))
        return 
        
    def refresh_auth(self):
        self.headers["Authorization"] = self.auth
        
        url = API[HOST] \
            + API[AUTH]["token"]
        
        payload = {
            "grant_type": "authorization_code",
            "refresh_token": self.token.refresh
        }
        resp = self.connection.post(url=url, data=payload, headers=self.headers)
        
        assert resp.status_code == 200, "Não foi possível criar token de acesso"
        self.token.set(json.loads(resp.content))
    
    def action(self, op_type,  operation, data={}):
        if(self.token.expires()):
            self.refresh_auth()
        
        self.headers["Authorization"] = f"Bearer {self.token.access}"
        
        url = API[HOST] \
            + operation
        return self.connection.request(op_type, url=url, data=data, headers=self.headers)
   
if (__name__ == "__main__"):
    import ipdb;ipdb.set_trace()
    r = RequestBing()
    print("Fim")