# app/services/frame_processing_service.py

from datetime import datetime
import cv2
import numpy as np
from app.models.emotion_model import EmotionModel
from app.schemas.api.history import HistoryRecordCreate
from app.services.history_repository import history_repo
from app.schemas.core import DetectionType
from typing import Dict

async def process_video_frame(frame: np.ndarray, emotion_model: EmotionModel) -> Dict:
    """
    Procesa un frame de video y guarda los resultados en el historial
    
    Args:
        frame: Frame de video en formato numpy array (OpenCV)
        emotion_model: Instancia del modelo de emociones
        
    Returns:
        Dict con los resultados del procesamiento
    """
    # Procesar el frame con el modelo de emociones
    raw_faces = emotion_model.predict_emotion(frame)
    
    # Convertir resultados a formato compatible con JSON
    processed_faces = []
    for face in raw_faces:
        processed_face = {
            "box": {
                "x": int(face["box"]["x"]),
                "y": int(face["box"]["y"]),
                "width": int(face["box"]["width"]),
                "height": int(face["box"]["height"])
            },
            "scores": {k: float(v) for k, v in face["scores"].items()},
            "dominant_emotion": str(face["dominant_emotion"])
        }
        processed_faces.append(processed_face)
    
    # Guardar en historial si se detectaron rostros
    if raw_faces:
        dominant_face = max(raw_faces, key=lambda x: max(x["scores"].values()))
        
        record_data = HistoryRecordCreate(
            timestamp=datetime.utcnow(),
            dominant_emotion=dominant_face["dominant_emotion"],
            emotion_scores=dominant_face["scores"],
            detection_type=DetectionType.VIDEO,
            image_snapshot=history_repo.image_to_base64(frame)
        )
        
        await history_repo.create_record(record_data)
    
    return {
        "faces": processed_faces,
        "frame_size": {
            "height": int(frame.shape[0]),
            "width": int(frame.shape[1])
        },
        "success": True,
        "timestamp": datetime.utcnow().isoformat()
    }

async def process_uploaded_video_frame(
    file_contents: bytes,
    emotion_model: EmotionModel  # Recibe el modelo inyectado
) -> Dict:
    """
    Procesa un frame de video subido como bytes
    
    Args:
        file_contents: Contenido del archivo subido (bytes)
        emotion_model: Modelo de emociones inyectado
        
    Returns:
        Dict con los resultados del procesamiento
    """
    nparr = np.frombuffer(file_contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if frame is None:
        raise ValueError("No se pudo decodificar la imagen")
    
    # Usamos el modelo inyectado en lugar de crear uno nuevo
    return await process_video_frame(frame, emotion_model)