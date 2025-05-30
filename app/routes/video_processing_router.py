from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models.emotion_model import EmotionModel
from app.services.frame_processing_service import process_uploaded_video_frame
from app.schemas.api.video_processing import ProcessResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

def get_emotion_model() -> EmotionModel:
    return EmotionModel()

@router.post("/process-frame", response_model=ProcessResponse)
async def process_frame(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        return await process_uploaded_video_frame(contents)
    except Exception as e:
        logger.error(f"Error processing frame: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))