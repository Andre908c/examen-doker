import json
import unittest
from unittest.mock import MagicMock, patch

from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_index_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    @patch("app.get_connection")
    def test_listar_productos(self, mock_get_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            {"id": 1, "nombre": "Laptop", "categoria": "Computo", "precio": "999.99"}
        ]

        response = self.client.get("/api/productos")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["nombre"], "Laptop")

    @patch("app.get_connection")
    def test_guardar_producto_exitoso(self, mock_get_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.lastrowid = 10

        payload = {
            "nombre": "Monitor",
            "categoria": "Perifericos",
            "precio": 250.0,
        }
        response = self.client.post(
            "/api/productos",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data["id"], 10)
        self.assertEqual(data["nombre"], "Monitor")

    def test_guardar_producto_validacion_campos_faltantes(self):
        payload = {"nombre": "", "categoria": "Perifericos", "precio": 100}
        response = self.client.post(
            "/api/productos",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_guardar_producto_validacion_precio_negativo(self):
        payload = {"nombre": "Teclado", "categoria": "Perifericos", "precio": -10}
        response = self.client.post(
            "/api/productos",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
