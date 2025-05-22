## @file: app/services/image_processing_service.py

from datetime import datetime
import uuid
import cv2
import numpy as np
from app.models.emotion_model import EmotionModel
from app.schemas.api.history import HistoryRecordCreate
from app.services.history_repository import history_repo
from app.schemas.core import DetectionType
from typing import Dict

async def process_image(image: bytes, emotion_model: EmotionModel) -> Dict:
    nparr = np.frombuffer(image, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if frame is None:
        raise ValueError("No se pudo decodificar la imagen")
    
    raw_faces = emotion_model.predict_emotion(frame)
    
    detections = []    
    for face in raw_faces:
        # Guardar en historial
        record_data = HistoryRecordCreate(
            dominant_emotion=face["dominant_emotion"],
            emotion_scores=face["scores"],
            detection_type=DetectionType.IMAGE,
            image_snapshot=history_repo.image_to_base64(frame)
        )
        await history_repo.create_record(record_data)
        
        # Preparar respuesta
        detection = {
            "faceId": str(uuid.uuid4()),
            "emotions": {k: float(v) for k, v in face["scores"].items()},
            "dominantEmotion": str(face["dominant_emotion"]),
            "timestamp": datetime.utcnow().isoformat(),
            "boundingBox": {
                "x": int(face["box"]["x"]),
                "y": int(face["box"]["y"]),
                "width": int(face["box"]["width"]),
                "height": int(face["box"]["height"])
            }
        }
        detections.append(detection)
    
    return {
        "detections": detections,
        "frameInfo": {
            "height": int(frame.shape[0]),
            "width": int(frame.shape[1]),
            "channels": int(frame.shape[2]) if len(frame.shape) > 2 else 1
        }
    }