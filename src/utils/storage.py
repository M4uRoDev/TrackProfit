import json

class SimpleStorage:
    """
    Clase de almacenamiento simple para pruebas.
    """

    def save(self, data):
        """
        Guarda los datos recolectados (simulado con impresión en consola).
        :param data: Datos recolectados para almacenar.
        """
        print("Guardando datos recolectados...")
        for entry in data:
            print(f"Fuente: {entry['source']}")
            print(f"Timestamp: {entry['timestamp']}")
            # Usar json.dumps para imprimir los datos en formato legible
            print("Datos:")
            print(json.dumps(entry['data'], indent=4))  # Formato con indentación
