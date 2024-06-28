from fastapi import FastAPI, Request
from app.api import router as api_router
from app.db import init_db
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings
import os
import sys
from fastapi.logger import logger
from pyngrok import ngrok
from app.api_server import server as api_server
import uvicorn
import threading

# Inicializar la base de datos\



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

init_db()

server = FastAPI()
app.include_router(api_router)
server.mount("/static", StaticFiles(directory="static"), name="static")



server.include_router(api_server)
# Incluir las rutas de la API


def run_app():
    uvicorn.run(app, host="0.0.0.0", port=8000)

def run_server():
    http_tunnel = ngrok.connect(3000)
    print(f"App2 public URL: {http_tunnel.public_url}")
    uvicorn.run(server, host="0.0.0.0", port=3000)

if __name__ == "__main__":
    thread1 = threading.Thread(target=run_app)
    thread2 = threading.Thread(target=run_server)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()