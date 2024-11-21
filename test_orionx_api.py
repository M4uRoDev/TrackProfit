from src.apis.orionx_api import OrionxAPI
from src.utils.config_loader import ConfigLoader

def test_orionx_api():
    config = ConfigLoader()
    api_key = config.get_env_var('ORIONX_API_KEY')
    api_secret = config.get_env_var('ORIONX_API_SECRET')

    orionx = OrionxAPI(api_key, api_secret)

    try: 
        getCurrency = orionx.get_currency("BTC")
        getCurrencyFactor = orionx.get_currencyTransformFactor("BTC", "CLP")
        print("Respuesta de la API:", getCurrency['data']['currency']['myWallet']['balance'] * getCurrencyFactor['data']['currencyTransformFactor']['factor'])
    except Exception as e:
        print("Error en la API:", e)

if __name__ == "__main__":
    test_orionx_api()