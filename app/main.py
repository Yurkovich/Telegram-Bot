from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from urls import task_template
from routers import router
from database import create_table


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(task_template)
app.include_router(router)


if __name__ == '__main__':
    create_table()
    print('Starting server')
    uvicorn.run('main:app', port=8000, reload=True)
    print('Server stopped')
