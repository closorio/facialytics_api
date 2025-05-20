## @file app/routes/image_processing_router.py

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.schemas.api.image_processing import DetectionResponse
from app.models.emotion_model import EmotionModel
from app.services.image_processing_service import process_image
from app.services.history_repository import save_to_history
from typing import Annotated

router = APIRouter()

# Dependency para el modelo de emociones
def get_emotion_model():
    model = EmotionModel()
    return model

@router.post("/process-image", response_model=DetectionResponse)
async def process_image_route(
    file: Annotated[UploadFile, File(description="Imagen para analizar emociones")],
    emotion_model: EmotionModel = Depends(get_emotion_model)
):
    try:
        # Leer imagen
        image = await file.read()
        
        # Procesar imagen
        result = await process_image(image, emotion_model)
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar la imagen: {str(e)}"
        )