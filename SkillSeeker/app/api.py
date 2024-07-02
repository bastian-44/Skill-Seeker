from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordRequestForm
from .auth import get_password_hash, verify_password
from .models import Planner, Request, WorkshopLeader, User
from .db import get_db
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request as FAPIRequest
router = APIRouter()

router.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@router.post("/register")
async def register(rut: str = Form(...), name: str = Form(...), password: str = Form(...)):
    user = User(name=name, rut=rut, password=password)
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM Planner WHERE rut = ?", (user.rut,))
    rows = cur.fetchall()

    if rows:
        db.close()
        raise HTTPException(status_code=400, detail="rut already registered")
    hashed_password = get_password_hash(user.password)
    cur.execute("INSERT INTO Planner (rut, name, password) VALUES (?, ?, ?)", (user.rut, user.name, hashed_password))
    print("hola")
    db.commit()
    db.close()

    return {"msg": "User registered successfully"}



@router.post("/login")
async def login_(username: str = Form(...), password: str = Form(...)):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM Planner WHERE rut = ?", (username,))
    user = cur.fetchone()
    db.close()
    if user is None or not verify_password(password, user[3]):
        raise HTTPException(status_code=400, detail="Incorrect rut or password")
    else:
        return user[0]

@router.post("/request")
async def request(request: Request):
    if not request.description.strip():  # Si la descripción está vacía o contiene solo espacios en blanco
        raise HTTPException(status_code=400, detail="Description cannot be empty")
     # Verificar si el planificador con el ID proporcionado existe en la base de datos
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM Planner WHERE id = ?", (request.planner_id,))
    count = cur.fetchone()[0]
    if count == 0:
        db.close()
        raise HTTPException(status_code=404, detail="Planner not found")
    cur.execute("INSERT INTO Requests (description, planner_id) VALUES (?, ?)", (request.description, request.planner_id))
    last_id = cur.lastrowid
    db.commit()
    db.close()

    return last_id

@router.post("/workshopleader")
async def workshopLeader(workshop_leader: WorkshopLeader):
    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO WorkshopLeader (name, description, phone, email, networks, request_id) VALUES (?, ?, ?, ?, ?, ?)", (workshop_leader.name, workshop_leader.description, workshop_leader.phone, workshop_leader.email, workshop_leader.networks, workshop_leader.request_id))
    db.commit()
    db.close()
    return {"msg": "Workshop leader added successfully"}

@router.get('/requesthistory')
async def requesthistory(planner_id: int):
    # Verificar si el planificador existe
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM Planner WHERE id = ?", (planner_id,))
    planner_exists = cur.fetchone()[0]
    if not planner_exists:
        db.close()
        raise HTTPException(status_code=404, detail="Planner not found")

    # Si el planificador existe, obtener su historial de solicitudes
    cur.execute("SELECT * FROM Requests WHERE planner_id = ?", (planner_id,))
    requests = cur.fetchall()
    db.close()
    return requests
@router.get('/workshopleaderhistory')
async def workshopleaderhistory(request_id: int):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM WorkshopLeader WHERE request_id = ?", (request_id,))
    workshop_leaders = cur.fetchall()
    db.close()
    return workshop_leaders

@router.get('/workshopleaderhistoryglobal')
async def workshopleaderhistory():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM WorkshopLeader WHERE favorite = ?", (1,))
    workshop_leaders = cur.fetchall()
    db.close()
    return workshop_leaders

@router.put('/favorite/{workshop_leader_id}')
async def favorite(workshop_leader_id: int):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE WorkshopLeader SET favorite = ? WHERE id = ?", (1, workshop_leader_id))
    db.commit()
    db.close()
    return {"message": "Favorite updated successfully"}

@router.put('/unfavorite/{workshop_leader_id}')
async def favorite(workshop_leader_id: int):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE WorkshopLeader SET favorite = ? WHERE id = ?", (0, workshop_leader_id))
    db.commit()
    db.close()
    return {"message": "Unfavorite updated successfully"}

@router.put('/contacted/{workshop_leader_id}')
async def favorite(workshop_leader_id: int):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE WorkshopLeader SET contacted = ? WHERE id = ?", (1, workshop_leader_id))
    db.commit()
    db.close()
    return {"message": "Contacted updated successfully"}

@router.get("/", response_class=HTMLResponse)
async def read_item(request: FAPIRequest):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

@router.get("/menu", response_class=HTMLResponse)
async def read_item(request: FAPIRequest):
    return templates.TemplateResponse(
        request=request, name="menu.html"
    )
@router.get("/menu/request", response_class=HTMLResponse)
async def read_item(request: FAPIRequest):
    return templates.TemplateResponse(
        request=request, name="request.html"
    )

@router.get("/menu/history", response_class=HTMLResponse)
async def read_item(request: FAPIRequest):
    return templates.TemplateResponse(
        request=request, name="history.html"
    )

@router.get("/menu/globalh", response_class=HTMLResponse)
async def read_item(request: FAPIRequest):
    return templates.TemplateResponse(
        request=request, name="globalh.html"
    )
