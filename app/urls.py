from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

task_template = APIRouter()
templates = Jinja2Templates(directory='templates')


@task_template.get('/')
def index():
    return RedirectResponse(url="/music")


@task_template.get('/signup')
def signup(request: Request):
    return templates.TemplateResponse(request=request, name='signup.html')


@task_template.get('/login')
def login(request: Request):
    return templates.TemplateResponse(request=request, name='login.html')


@task_template.get('/music')
def login(request: Request):
    return templates.TemplateResponse(request=request, name='music.html')
