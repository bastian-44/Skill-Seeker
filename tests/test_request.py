import unittest
import requests


class TestRequestEndopoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base_url = "http://localhost:8000" #URL base de la aplicación
        cls.description = "This is a valid description" #Descripción válida para la solicitud
        cls.description_empty = "" #Descripción vacía para probar la solicitud con descripción vacía
        cls.planner_id = 1 #ID de un planificador válido
        cls.planner_id_invalid = 9999 #ID de un planificador no válido 

    @classmethod
    def tearDownClass(cls) -> None:
        #Limpiar atributos de clase al finalizar las pruebas
        del cls.description
        del cls.description_empty
        del cls.planner_id
        del cls.planner_id_invalid

    #Prueba para verificar que se genera una request correctamente
    def test_request_succesful(self):
        #Prueba una solicitud exitosa con descripción válida y ID de planificador válido
        response = requests.post(f"{self.base_url}/request", json={"description": self.description, "planner_id": self.planner_id,  "request_id": 0})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), int)
        #Verifica que la solicitud devuelve un código de estado 200 (OK)
        #Verifica que la respuesta contiene el ID de la solicitud creada
        pass

    #Prueba para verificar que no se puede generar una request dado que se le entrega una descripción vacía
    def test_request_description_empty(self):
        #Prueba una solicitud con descripción vacía
        response = requests.post(f"{self.base_url}/request", json={"description": self.description_empty, "planner_id": self.planner_id,  "request_id": 0})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Description cannot be empty"})
        #Verifica que la solicitud devuelve un código de estado 400 (Bad Request)
        #Verifica que la respuesta contiene el mensaje de error adecuado
        pass

    #Prueba para verificar que no se puede generar una request dado que se le entrega un planificador inexistente/invalido
    def test_invalid_planner_id_request(self):
        #Prueba una solicitud con un ID de planificador no válido
        response = requests.post(
            f"{self.base_url}/request",
            json={"description": self.description, "planner_id": self.planner_id_invalid, "request_id": 0}
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Planner not found"})
        #Verifica que la solicitud devuelve un código de estado 404 (Not Found)
        #Verifica que la respuesta contiene el mensaje de error adecuado
        pass

if __name__ == '__main__':
    unittest.main()