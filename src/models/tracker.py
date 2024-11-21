import datetime

from models.source import DataSource

# TODO: Añadir validaciones para asegurar que las monedas en la configuración sean soportadas por API OrionxAPI
# TODO: Probar Tracker con otras fuentes de datos
# TODO: Implementar métodos de almacenamiento en Storage

class Tracker:

    def __init__(self, sources=None, storage=None):
        """
        Inicializa la instancia de la clase Tracker
        :param sources: Lista de fuentes de datos
        :param storage: Instancia de clase Storage
        """
        self.sources = sources if sources else []
        self.storage = storage
    
    def add_source(self, source):
        """
        Agrega una fuente de datos a la lista de fuentes
        :param source: Instancia de clase Source (e.g., OrionxAPI)
        """
        if not isinstance(source, DataSource): 
            raise TypeError("La fuente debe ser una instancia de DataSource")
        self.sources.append(source)

    def collect_data(self, config=None):
        """
        Recolecta datos de todas las fuentes y los almacena
        :return: Diccionario con los datos recolectados
        """
        results = []
        for source in self.sources:
            try:
                # Obtener configuración específica de la fuente, si está disponible
                source_config = config.get(source.__class__.__name__, {}) if config else {}
                data = source.fetch_data(**source_config)  # Pasar configuración a la fuente
                results.append({
                    "source": source.__class__.__name__,
                    "timestamp": datetime.datetime.now().isoformat(),
                    "data": data["data"]
                })
            except Exception as e:
                print(f"Error al obtener datos de {source.__class__.__name__}: {e}")
        return results
        

    def save_data(self, data):
        """
        Guarda los datos recolectados en el almacenamiento configurado
        :param data: Diccionario con los datos recolectados
        """
        if self.storage: 
            try: 
                self.storage.save(data)
            except Exception as e:
                print(f"Error al guardar los datos: {e}")
        else: 
            print("No se ha configurado un almacenamiento")

    def run(self, config=None):
        """
        Ejecuta la recolección y almacenamiento de datos.
        """
        print("Iniciando recolección de datos...")
        data = self.collect_data(config=config)
        if data:
            # print(f"Datos recolectados: {data}")
            self.save_data(data)
        else: print("No se han recolectado datos")