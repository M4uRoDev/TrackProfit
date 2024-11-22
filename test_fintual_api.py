from src.apis.fintual_api import FintualAPI
from src.utils.config_loader import ConfigLoader

def test_fintual_api():
    config = ConfigLoader()
    email = config.get_env_var('FINTUAL_EMAIL')
    password = config.get_env_var('FINTUAL_PASSWORD')

    fintual = FintualAPI(email, password)

    try: 
        token = fintual.get_goals()
        print("Token de acceso:", token)
    except Exception as e:
        print("Error en la API:", e)

if __name__ == "__main__":
    test_fintual_api()