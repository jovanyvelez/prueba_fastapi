from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel


# Modelo de datos
class Perro(BaseModel):
    id: int | None = None
    nombre: str
    raza: str

# Inicializar FastAPI
app = FastAPI(title="CRUD de Perros")

# Configurar templates
templates = Jinja2Templates(directory="templates")

# Lista en memoria para almacenar los perros
perros_db: list[Perro] = []
next_id = 1


# Funciones auxiliares
def obtener_perro_por_id(perro_id: int) -> Perro | None:
    for perro in perros_db:
        if perro.id == perro_id:
            return perro
    return None

def obtener_siguiente_id() -> int:
    global next_id
    current_id = next_id
    next_id += 1
    return current_id

# Rutas del CRUD

@app.get("/", response_class=HTMLResponse)
async def listar_perros(request: Request):
    """Mostrar la lista de perros en la página principal"""
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "perros": perros_db}
    )

@app.get("/crear", response_class=HTMLResponse)
async def mostrar_formulario_crear(request: Request):
    """Mostrar formulario para crear un nuevo perro"""
    return templates.TemplateResponse(
        "crear.html", 
        {"request": request}
    )

@app.post("/crear")
async def crear_perro(nombre: str = Form(...), raza: str = Form(...)):
    """Crear un nuevo perro"""
    nuevo_perro = Perro(
        id=obtener_siguiente_id(),
        nombre=nombre,
        raza=raza
    )
    perros_db.append(nuevo_perro)
    return RedirectResponse(url="/", status_code=303)

@app.get("/editar/{perro_id}", response_class=HTMLResponse)
async def mostrar_formulario_editar(request: Request, perro_id: int):
    """Mostrar formulario para editar un perro"""
    perro = obtener_perro_por_id(perro_id)
    if not perro:
        raise HTTPException(status_code=404, detail="Perro no encontrado")
    
    return templates.TemplateResponse(
        "editar.html", 
        {"request": request, "perro": perro}
    )

@app.post("/editar/{perro_id}")
async def editar_perro(perro_id: int, nombre: str = Form(...), raza: str = Form(...)):
    """Actualizar un perro existente"""
    perro = obtener_perro_por_id(perro_id)
    if not perro:
        raise HTTPException(status_code=404, detail="Perro no encontrado")
    
    perro.nombre = nombre
    perro.raza = raza
    return RedirectResponse(url="/", status_code=303)

@app.post("/eliminar/{perro_id}")
async def eliminar_perro(perro_id: int):
    """Eliminar un perro"""
    perro = obtener_perro_por_id(perro_id)
    if not perro:
        raise HTTPException(status_code=404, detail="Perro no encontrado")
    
    perros_db.remove(perro)
    return RedirectResponse(url="/", status_code=303)



