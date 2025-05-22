## @file app/routes/history_router.py

from fastapi import APIRouter, Query, HTTPException
from app.schemas.api.history import HistoryResponse
from app.services.history_repository import history_repo
from typing import Optional
from app.schemas.core import DetectionType 

router = APIRouter()

@router.get("/", response_model=HistoryResponse)
async def read_history(
    page: Optional[int] = Query(None, ge=1, description="Número de página para paginación"),
    per_page: Optional[int] = Query(10, ge=1, le=50, description="Elementos por página (máx. 50)"),
    detection_type: Optional[DetectionType] = Query(
        None, 
        description="Filtrar por tipo de detección: 'image' o 'video'"
    )
):
    try:
        records = await history_repo.get_history(
            page=page,
            per_page=per_page,
            detection_type=detection_type.value if detection_type else None
        )
        total = len(history_repo._history)
        
        return HistoryResponse(
            records=records,
            total=total,
            page=page,
            per_page=per_page
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/", status_code=204)
async def delete_history():
    await history_repo.clear_history()
    return None