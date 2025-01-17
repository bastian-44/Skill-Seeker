import requests
from pydantic import BaseModel
from typing import Optional
from config.config import bing_search_api_key, bing_search_endpoint
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown

class Planner(BaseModel):
    name: str
    rut: str
    id: int

class Request(BaseModel):
    description: str
    planner_id: int
    request_id: int

class WorkshopLeader(BaseModel):
    name: str
    description: str
    phone: str
    email: str
    networks: str
    favorite: int = 0
    contacted: int = 0

class User(BaseModel):
    name: str
    rut: str
    password: str

    
class Planner:
    request: None
    def __init__(self, name, rut, id):
        self.name = name
        self.rut = rut
        self.id = id

    def getId(self):
        return self.id
    def generateRequest(self, query, planner_id, request_id):
        self.request = Request(description=query, planner_id=planner_id, request_id=request_id)
        self.request.aiCall()

class WorkshopLeader(BaseModel):
    name: str
    description: str
    phone: str
    email: str
    networks: str
    request_id: int
    favorite: int = 0
    contacted: int = 0

class Request(BaseModel):
    description: str
    planner_id: int
    request_id: Optional[int]


    def getId(self):
        return self.request_id
    
    def aiCall(self):
        extract = AiExtractor(self.description, self)
    

    def addWorkshopLeader(self, name: str, description: str, phone: str, email: str, networks:str, request_id: int):
        workshop_leader = WorkshopLeader(name=name, description=description, phone=phone, email=email, networks=networks, request_id=request_id)
        response = requests.post("http://localhost:8000/workshopleader", json={"name": name, "description": description, "phone": phone, "email": email, "networks": networks, "request_id": request_id})
    
        
class AiExtractor:
    def __init__(self, query, request):

        genai.configure(api_key = google_api)
        modelo = genai.GenerativeModel('gemini-pro')

        def to_markdown(text):
            text = text.replace('•', '  *')
            return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
        
        respuesta = modelo.generate_content('Extrae la información del siguiente texto y quiero que la entregues en el siguiente formato: '
                        'Taller, Descripción del taller, descripción del líder del taller, Chile. '
                        'El taller debería incluir en menos de 3 palabras a qué taller se refiere, la descripción del taller es lo que se hará en él, '
                        'la descripción del líder del taller es lo que se espera que el líder del taller sepa hacer para la realización del taller y Chile es para referenciar que la búsqueda será en Chile. '
                        'El texto es el siguiente: ' + query)

        
        self.searcher = Searcher(respuesta.text, request)

class Searcher:
    def __init__(self, query, request):
        # Construct a request
        self.query = 'site:linkedin.com/in/ '
        self.query += query
        mkt = 'cl-ES'
        params = {'q': self.query, 'mkt': mkt}
        headers = {'Ocp-Apim-Subscription-Key': bing_search_api_key}

        # Call the API
        try:
            response = requests.get(bing_search_endpoint,
                                    headers=headers, params=params)
            response.raise_for_status()
            json = response.json()
            result = Results(json["webPages"]["value"], request)


        except Exception as ex:
            raise ex

class Results:

    def __init__(self, text, request):
        self.text = text
        self.request = request
        x= 0
        while x < 8:
            items = text[x]
            self.request.addWorkshopLeader(items['name'], items['snippet'], '', '', items['url'], self.request.getId())
            x += 1


class Contact:
    def __init__(self, phone, email, networks):
        self.phone = phone
        self.email = email
        self.networks = networks


