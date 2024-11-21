from abc import ABC, abstractmethod

class DataSource(ABC):

    """ 
    Interfaz generica para fuentes de datos.    
    """

    @abstractmethod
    def fetch_data(self):
        """
        Recolecta datos de la fuente y los retorna.
        :return: Diccionario con los datos recolectados
        """
        pass