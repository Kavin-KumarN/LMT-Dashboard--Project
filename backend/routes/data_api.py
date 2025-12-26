from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

from backend.services.data_service import load_data, apply_filters

router = APIRouter()

UPLOAD_DIR = "frontend/uploaded_files"

# ---------------------------
# Request Model
# ---------------------------
class DataRequest(BaseModel):
    file_name: str
    filters: dict = {}

# ---------------------------
# Get Filtered Data
# ---------------------------
@router.post("/api/data")
def get_data(request: DataRequest):
    try:
        df = load_data(request.file_name)
        df = apply_filters(df, request.filters)
        return df.to_dict(orient="records")

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------
# List Uploaded Files
# ---------------------------
@router.get("/api/files")
def list_uploaded_files():
    if not os.path.exists(UPLOAD_DIR):
        return []

    return [
        f for f in os.listdir(UPLOAD_DIR)
        if f.lower().endswith((".csv", ".xlsx", ".xls"))
    ]

# ---------------------------
# Delete File
# ---------------------------
@router.delete("/api/files/{file_name}")
def delete_file(file_name: str):
    path = os.path.join(UPLOAD_DIR, file_name)

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")

    os.remove(path)
    return {"message": "File deleted successfully"}
