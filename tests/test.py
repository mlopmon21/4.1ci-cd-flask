import unittest
from src.app import app


class BasicTests(unittest.TestCase):

    def setUp(self):
        # Crea un cliente de prueba usando la aplicación Flask
        self.app = app.test_client()
        self.app.testing = True

    def test_home(self):
        # Envía una solicitud GET a la ruta '/'
        result = self.app.get('/')

        # Verifica que la respuesta sea "Hello, World!"
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data.decode(), "Hello, World!")

# Tests adicionales (Práctica 4.1)

class ExtraTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_not_found_returns_404(self):
        result = self.app.get('/ruta-que-no-existe')
        self.assertEqual(result.status_code, 404)

    def test_home_content_type(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        # Aceptamos HTML/texto o JSON
        self.assertTrue(
            "text" in result.content_type or "html" in result.content_type or "json" in result.content_type
        )

    def test_home_not_empty(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertTrue(len(result.data) > 0)


if __name__ == "__main__":
    unittest.main()
