from fastapi import APIRouter, UploadFile, File
from app.explain_utils import process_zip_and_explain, explain_single_code_file
import os

router = APIRouter()

@router.post("/upload")
async def explain_upload(file: UploadFile = File(...)):
    filename = file.filename.lower()

    os.makedirs("temp_uploads", exist_ok=True)
    save_path = os.path.join("temp_uploads", file.filename)

    with open(save_path, "wb") as f:
        f.write(await file.read())

    if filename.endswith(".zip"):
        results = process_zip_and_explain(save_path)
        return {"type": "zip", "results": results}

    elif filename.endswith((".py", ".js", ".ts", ".json", ".html", ".java", ".css", ".txt")):
        with open(save_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        explanation = explain_single_code_file(file.filename, content)
        return {"type": "single_file", "file": file.filename, "explanation": explanation}

    else:
        return {"error": "Unsupported file type. Please upload a .zip or code file."}
