import unittest
import requests
from src.main import app


class TestRequestEndopoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base_url = "http://localhost:8000"  # URL base de tu aplicación

        pass

    @classmethod
    def tearDown(cls) -> None:
        pass

    def test_request_succesful(self):
        description = "This is a valid description"
        planner_id = 1  # ID de planificador válido



        response = requests.post(f"{self.base_url}/request", json={"description": description, "planner_id": planner_id})
        self.assertEqual(response.status_code, 200)

        # Verificar que la respuesta contiene el ID de la solicitud creada
        self.assertIn("id", response.json())
        request_id = response.json()["id"]

        pass

if __name__ == '__main__':
    unittest.main()
