from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers import todos, auth, upload_download, testhtml

app = FastAPI(title="TODOLIST API")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(todos.router)
app.include_router(auth.router)
app.include_router(upload_download.router)
app.include_router(testhtml.router)
