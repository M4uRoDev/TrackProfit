import os
import sqlite3

from typing import List, Dict

class SQLiteStorage:
    """
    Clase para manejar el almacenamiento de datos en una base de datos SQLite.
    """

    def __init__(self, db_path="db/data.db"):
        """
        Inicializa la instancia de la clase SQLiteStorage.
        :param db_path: Ruta al archivo de base de datos SQLite.
        """
        db_folder = os.path.dirname(db_path)
        if db_folder:
            os.makedirs(db_folder, exist_ok=True)
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        """
        Crea la tabla assets si no existe.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS assets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT NOT NULL,
                    asset TEXT NOT NULL,
                    type TEXT NOT NULL,
                    amount REAL NOT NULL,
                    currency TEXT NOT NULL,
                    factor REAL,
                    timestamp TEXT NOT NULL
                )
            """)
            conn.commit()

    def save(self, data: List[Dict]):
        """
        Guarda los datos en la tabla assets.
        :param data: Lista de diccionarios con datos estandarizados.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for entry in data:
                for asset in entry["data"]:
                    cursor.execute("""
                        INSERT INTO assets (source, asset, type, amount, currency, factor, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        entry["source"],        # Fuente del dato
                        asset["asset"],         # Activo
                        asset["type"],          # Tipo de activo
                        asset["amount"],        # Cantidad
                        asset["currency"],      # Divisa del amount
                        asset.get("factor"),    # Factor de conversión
                        entry["timestamp"]      # Timestamp general
                    ))
            conn.commit()

    def fetch_all(self):
        """
        Recupera todos los datos almacenados en la tabla assets.
        :return: Lista de diccionarios con los datos recuperados.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM assets")
            return cursor.fetchall()