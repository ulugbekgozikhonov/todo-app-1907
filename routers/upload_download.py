import shutil
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

router = APIRouter(tags=["upload-download"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
	filename = file.filename
	filepath = UPLOAD_DIR / filename

	if not file.content_type in ["JPEG", "JPG", "GIF", "PNG", "MOV"]:
		raise HTTPException(status_code=404, detail="File type not supported.")

	with filepath.open("wb") as buffer:
		shutil.copyfileobj(file.file, buffer)

	return {"filename": filename, "filesize": filepath.stat().st_size}


@router.get("/download/{filename}")
async def download_file(filename: str):
	filename = Path(filename)
	filepath = UPLOAD_DIR / filename
	if not filepath.is_file():
		raise HTTPException(status_code=404, detail="File not found")

	return FileResponse(filepath)
