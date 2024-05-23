from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

task_template = APIRouter()
templates = Jinja2Templates(directory='templates')


@task_template.get('/')
def index(request: Request):
    return templates.TemplateResponse(request=request, name='index.html')
