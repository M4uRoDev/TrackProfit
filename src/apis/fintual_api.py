import requests
import ujson
import time

from models.source import DataSource
from datetime import datetime

class FintualAPI(DataSource):
    BASE_URL = "https://fintual.cl/api"
    TOKEN = ""

    def __init__(self, email, password):
        """
        Inicializa la instancia de la clase FintualAPI
        :param email: Correo electronico de la cuenta de Fintual.
        :param password: Contraseña de la cuenta de Fintual.
        """
        self.email = email
        self.password = password
        self.get_access_token()

    def set_headers(self):
        """
        Funcion que genera el header necesario para la peticion
        """
        return {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def get_access_token(self):
        """
        Funcion que obtiene el token de acceso
        para consumir la API
        """
        query = {
            "user": {
                "email": self.email,
                "password": self.password
            }
        }

        headers = self.set_headers()

        body = ujson.dumps(query)

        response = requests.post(self.BASE_URL + "/access_tokens", headers=headers, data=body)
        response.raise_for_status()

        if response.status_code == 201:
            self.TOKEN = response.json()['data']['attributes']['token']
            return self.TOKEN
        
    def get_goals(self):
        """
        Funcion que obtiene los goals de fintual
        """
        headers = self.set_headers()

        params = {
            "user_email": self.email,
            "user_token": self.TOKEN
        }

        response = requests.get(self.BASE_URL + "/goals", headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def fetch_data(self):
        """
        Implementa el contrato de DataSource
        Recolecta los datos de Fintual asociados a los GOALS definidos.
        :return: Diccionario con los datos recolectados
        """
        standardized_data = []

        try: 
            goals = self.get_goals()
            for goal in goals['data']:
                standardized_data.append({
                    "asset": goal['attributes']['name'],
                    "type": "goal",
                    "amount": goal['attributes']['nav'],
                    "currency": "CLP",
                    "factor": 1,
                    "timestamp": datetime.now().isoformat()
                })
        except Exception as e:
            print(f"Error al obtener datos: {e}")

        return {
            "source": "FintualAPI",
            "data": standardized_data,
            "timestamp": datetime.now().isoformat()
        }


