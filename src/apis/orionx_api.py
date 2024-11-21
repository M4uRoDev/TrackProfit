import ujson 
import requests
import hmac
import time

# Se importa la funcion hash sha512
from hashlib import sha512
from models.source import DataSource
from datetime import datetime


class OrionxAPI(DataSource):

    BASE_URL = "https://api2.orionx.com/graphql"

    def __init__(self, api_key, api_secret):
        """
        Inicializa la instancia de la clase OrionxAPI
        :param api_key: Clave de API de Orionx.
        :param api_secret: Secreto de API de Orionx.
        """
        self.api_key = api_key
        self.api_secret = api_secret
    
    def hmac_sha512(self, secret_key, timestamp, body): 
        """
        Funcion que genera firma para consumo de API
        :param secret_key: Clave secreta de API
        :param timestamp: Marca de tiempo
        :param body: Cuerpo de la peticion
        """
        key = bytearray(secret_key, 'utf-8')
        msg = str(timestamp) + str(body)

        msg = msg.encode('utf-8')
        
        return hmac.HMAC(key, msg, sha512).hexdigest()

    def set_headers(self, body):
        """
        Funcion que genera el header necesario para la peticion
        """
        timestamp = str(int(time.time()))
        
        signature = str(self.hmac_sha512(self.api_secret, timestamp, body))

        headers = {
            "Content-Type": "application/json",
            "X-ORIONX-TIMESTAMP": timestamp,
            "X-ORIONX-APIKEY": self.api_key,
            "X-ORIONX-SIGNATURE": signature
        }
        return headers
    
    def get_currency(self, code):
        query_str = '''
        query {
            currency(code: "%s") {
                code
                name
                symbol
                format
                longFormat
                isCrypto
                minimumAmountToSend
                units
                round
                myWallet {
                    _id
                    balance
                    availableBalance
                    unconfirmedBalance
                }
            }
        }''' % code

        query = {
            'query': query_str
        }

        body = ujson.dumps(query)
        headers = self.set_headers(body)

        response = requests.post(self.BASE_URL, headers=headers, data=body)
        response.raise_for_status()

        data = ujson.loads(response.text)

        if response.status_code == 200:
            return data
        else:
            raise Exception(f"Error: {response.status_code}: {response.text}")
        
    def get_currencyTransformFactor(self, code, toCode): 
        query_str = '''
        query {
            currencyTransformFactor(inCurrencyCode: "%s", outCurrencyCode: "%s"){
                factor
            }
        }''' % (code, toCode)

        query = {
            'query': query_str
        }

        body = ujson.dumps(query)
        headers = self.set_headers(body)

        response = requests.post(self.BASE_URL, headers=headers, data=body)
        response.raise_for_status()

        data = ujson.loads(response.text)

        if response.status_code == 200:
            return data
        else:
            raise Exception(f"Error: {response.status_code}: {response.text}")
    
    def fetch_data(self, currencies=None):
        """
        Implementa el contrato de DataSource 
        Recolecta datos relevantes de Orionx para las monedas especificadas.
        :param currencies: Lista de códigos de monedas a consultar (e.g., ["BTC", "ETH"])
        :return: Diccionario con los datos recolectados
        """

        if currencies is None:
            return {}
        
        standardized_data = []

        for currency in currencies:
            try: 
                currency_data = self.get_currency(currency)
                transform_factor = self.get_currencyTransformFactor(currency, 'CLP')

                standardized_data.append({
                    "asset": currency,
                    "type": "crypto",
                    "amount": currency_data['data']['currency']['myWallet']['balance'],
                    "currency": currency,
                    "factor": transform_factor['data']['currencyTransformFactor']['factor'],
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                print(f"Error al obtener datos: {e}")
        
        return {
            "source": "OrionxAPI",
            "data": standardized_data,
            "timestamp": datetime.now().isoformat()
        }
        