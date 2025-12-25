"""
Page routes for serving HTML templates
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import settings

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render homepage with plant disease detection UI"""
    return templates.TemplateResponse("index.html", {"request": request})
