from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from urls import task_template
from routers import router


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(task_template)
app.include_router(router)


if __name__ == '__main__':
    print('Starting server')
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
    print('Server stopped')
