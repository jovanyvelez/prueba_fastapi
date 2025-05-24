from fastapi import FastAPI, Request

from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates")

Saludo = "Somos los proximos Egresados de la Javiera"

@app.get("/")
async def inicio(request: Request):
    return templates.TemplateResponse("index.html", {"request": request,"Saludo": Saludo})