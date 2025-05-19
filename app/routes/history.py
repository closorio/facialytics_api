from fastapi import APIRouter, HTTPException
from app.services.storage import get_history, clear_history
from typing import List
from app.models.schemas import HistoryRecord

router = APIRouter()

@router.get("/", response_model=List[HistoryRecord])
async def read_history(limit: int = 10):
    return await get_history(limit)

@router.delete("/")
async def delete_history():
    await clear_history()
    return {"message": "Historial borrado"}