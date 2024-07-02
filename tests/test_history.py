import unittest
import requests



class TestHistoryEndopoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base_url = "http://localhost:8000"  #URL base de la aplicación
        cls.planner_id = 1  #ID de un planificador válido
        cls.planner_id_invalid = 99999 #ID de un planificador no válido 
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        #Limpiar atributos de clase al finalizar las pruebas
        del cls.planner_id 
        del cls.planner_id_invalid
        pass

    #Prueba para verificar que se obtiene un historial correctamente
    def test_history_succesful(self):
        #Prueba una solicitud exitosa conun ID de planificador válido
        response = requests.get(f"http://localhost:8000/requesthistory?planner_id={self.planner_id}")       
        self.assertEqual(response.status_code, 200)
        #Verifica que la solicitud devuelve un código de estado 200 (OK)
        pass

    #Prueba para verificar que no se puede obtener un historial dado que se le entrega un planificador inexistente/invalido
    def test_history_planner_id_inexistent(self):
        #Prueba una solicitud con un ID de planificador no válido
        response = requests.get(f"http://localhost:8000/requesthistory?planner_id={self.planner_id_invalid}")       
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Planner not found"})
        #Verifica que la solicitud devuelve un código de estado 404 (Not Found)
        #Verifica que la respuesta contiene el mensaje de error adecuado
        pass

    
if __name__ == '__main__':
    unittest.main()