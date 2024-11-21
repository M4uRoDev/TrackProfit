import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from utils.config_loader import ConfigLoader
import unittest
from unittest.mock import patch, mock_open

class TestConfigLoader(unittest.TestCase):

    def test_load_env_file_success(self):
        """Probar que el archivo .env se carga correctamente."""
        with patch("os.path.exists", return_value=True), \
             patch("utils.config_loader.load_dotenv") as mock_load_dotenv:
            config = ConfigLoader(".env")
            mock_load_dotenv.assert_called_with(".env")

    def test_load_env_file_not_found(self):
        """Probar que lanza un error si no encuentra el archivo .env."""
        with patch("os.path.exists", return_value=False):
            with self.assertRaises(FileNotFoundError):
                ConfigLoader(".env")

    def test_get_env_var_success(self):
        """Probar que get_env_var devuelve la variable correcta."""
        with patch("os.getenv", return_value="test_value"):
            value = ConfigLoader.get_env_var("TEST_VAR")
            self.assertEqual(value, "test_value")

    def test_get_env_var_default(self):
        """Probar que get_env_var devuelve el valor por defecto."""
        with patch("os.getenv", return_value="default_value"):
            value = ConfigLoader.get_env_var("TEST_VAR", default="default_value")
            self.assertEqual(value, "default_value")

    def test_get_env_var_missing(self):
        """Probar que get_env_var lanza un error si falta la variable."""
        with patch("os.getenv", return_value=None):
            with self.assertRaises(ValueError):
                ConfigLoader.get_env_var("MISSING_VAR")

if __name__ == "__main__":
    unittest.main()
