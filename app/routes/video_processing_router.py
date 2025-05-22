## @file app/routes/video_processing_router.py

import asyncio
import cv2
import logging
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from app.services.video_processing_service import WebcamService
from app.models.emotion_model import EmotionModel 
from typing import Annotated
from app.schemas.api.video_processing import ProcessResponse

router = APIRouter()
webcam_service = WebcamService()

def get_emotion_model() -> EmotionModel:
    """Función de dependencia para obtener una instancia del modelo de emociones"""
    return EmotionModel()

logger = logging.getLogger(__name__)

async def generate_frames():
    """Generador de frames para el stream MJPEG"""
    while True:
        try:
            frame = webcam_service.get_latest_frame()
            if frame is None:
                logger.warning("Frame vacío recibido")
                await asyncio.sleep(0.1)
                continue
                
            # Preprocesamiento
            frame = cv2.resize(frame, (640, 480))
            _, buffer = cv2.imencode('.jpg', frame, [
                cv2.IMWRITE_JPEG_QUALITY, 80
            ])
            
            yield (b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            
            await asyncio.sleep(0.033)  # Control de FPS
            
        except Exception as e:
            logger.error(f"Error en generate_frames: {str(e)}")
            await asyncio.sleep(1)

@router.get("/stream")
async def video_stream():
    """Endpoint para streaming de video"""
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )

@router.on_event("startup")
async def startup_event():
    webcam_service.start()

@router.on_event("shutdown")
async def shutdown_event():
    webcam_service.stop()

@router.get("/process-latest-frame", response_model=ProcessResponse)
async def process_latest_frame(
    emotion_model: Annotated[EmotionModel, Depends(get_emotion_model)]
):
    try:
        # Usamos el método process_frame que ya incluye la lógica para guardar en el historial
        result = await webcam_service.process_frame(emotion_model)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing frame: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar emociones: {str(e)}"
        )