from fastapi import FastAPI

from routers import todo, auth, upload_download

app = FastAPI(title="TODOLIST API")

@app.get("/ketmon",status_code=200)
async def ketmonjon():
	return {"status": "Salom Ketmon"}

app.include_router(todo.router)
app.include_router(auth.router)
app.include_router(upload_download.router)
