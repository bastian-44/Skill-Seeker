from fastapi import FastAPI, Request
from app.api import router as api_router
from app.db import init_db
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Inicializar la base de datos\
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")





init_db()

# Incluir las rutas de la API
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)