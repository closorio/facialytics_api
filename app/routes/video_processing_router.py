# app/routes/video_processing_router.py

from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from app.models.emotion_model import EmotionModel
from app.services.frame_processing_service import process_uploaded_video_frame
from app.schemas.api.video_processing import ProcessResponse
import logging
from typing import Annotated

router = APIRouter()
logger = logging.getLogger(__name__)

def get_emotion_model() -> EmotionModel:
    return EmotionModel()

@router.post("/process-frame", response_model=ProcessResponse)
async def process_frame(
    emotion_model: Annotated[EmotionModel, Depends(get_emotion_model)], 
    file: UploadFile = File(...) 
):
    try:
        contents = await file.read()
        # Pasamos el modelo inyectado en lugar de crear uno nuevo
        return await process_uploaded_video_frame(contents, emotion_model)
    except Exception as e:
        logger.error(f"Error processing frame: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))