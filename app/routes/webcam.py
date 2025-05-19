import asyncio
import cv2
import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.services.webcam_service import WebcamService
from app.models.emotion_model import EmotionModel 
from app.schemas import ProcessResponse 

router = APIRouter()
webcam_service = WebcamService()
emotion_model = EmotionModel() 
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
async def process_latest_frame():
    frame = webcam_service.get_latest_frame()
    if frame is None:
        raise HTTPException(status_code=404, detail="No se pudo capturar el frame")
    
    try:
        raw_faces = emotion_model.predict_emotion(frame)
        
        return ProcessResponse(
            faces=raw_faces,  # ← Ya tiene la estructura correcta
            frame_size={
                "height": int(frame.shape[0]),
                "width": int(frame.shape[1]),
                "channels": int(frame.shape[2]) if len(frame.shape) > 2 else 1
            },
            success=True
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar emociones: {str(e)}"
        )