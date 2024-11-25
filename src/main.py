from apis.orionx_api import OrionxAPI
from models.tracker import Tracker
from utils.config_loader import ConfigLoader
from utils.storage import SimpleStorage

def main():
    """
    Punto de entrada principal para TrackProfit
    """

    print("Iniciando TrackProfit...")

    # Cargar configuración
    config = ConfigLoader()

    # Configurar la API de Orionx
    orionx_api = OrionxAPI(
        api_key=config.get_env_var("ORIONX_API_KEY"),
        api_secret=config.get_env_var("ORIONX_API_SECRET")
    )

    # Configurar almacenamiento simple #TODO: Implementar almacenamiento en base de datos
    storage = SimpleStorage()

    # Inicializar el Tracker con Orionx como fuente
    tracker = Tracker(
        sources=[orionx_api],
        storage=storage
    )

    # Configurar monedas especificas para Orionx
    tracker_config = {
        "OrionxAPI": {
            "currencies": ["BTC", "CHA"]
        }
    }

    # Ejecutar el Tracker con la configuración
    tracker.run(config=tracker_config)

if __name__ == "__main__":
    main()

