from fastapi import FastAPI, Request

from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.routers.compare import router

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(router)

templates = Jinja2Templates(directory="src/templates")

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
