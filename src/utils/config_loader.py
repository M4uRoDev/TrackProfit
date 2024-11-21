import os
from dotenv import load_dotenv

class ConfigLoader:
    """
    Clase para cargar configuraciones y variables de entorno.
    """

    def __init__(self, env_file=".env"):
        """
        Inicializa el cargador de configuraciones.
        :param env_file: Ruta al archivo .env (por defecto, el archivo raíz).
        """
        self.env_file = env_file
        self._load_env_file()

    def _load_env_file(self):
        """
        Carga las variables del archivo .env.
        """
        if os.path.exists(self.env_file):
            load_dotenv(self.env_file)
        else:
            raise FileNotFoundError(f"No se encontró el archivo {self.env_file}")

    @staticmethod
    def get_env_var(var_name, default=None):
        """
        Obtiene una variable de entorno.
        :param var_name: Nombre de la variable.
        :param default: Valor por defecto si la variable no existe.
        :return: Valor de la variable de entorno o el valor por defecto.
        """
        value = os.getenv(var_name, default)
        if value is None:
            raise ValueError(f"La variable de entorno {var_name} no está configurada.")
        return value
