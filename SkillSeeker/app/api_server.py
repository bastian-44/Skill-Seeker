from fastapi import FastAPI, APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.db import get_db


server = APIRouter()

server.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@server.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="form.html"
    )

@server.post("/submit")
async def submit(nombre: str = Form(...), telefono: str = Form(...), mail: str = Form(...), titulo: str = Form(...), propuesta: str = Form(...)):
    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO Form (name, telefono, mail, titulo, propuesta) VALUES (?, ?, ?, ?, ?)", (nombre, telefono, mail, titulo, propuesta))
    db.commit()
    db.close()
    