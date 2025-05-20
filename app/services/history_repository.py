## @file app/services/history_repository.py

from datetime import datetime
from typing import List, Optional
from app.schemas.api.image_processing import DetectionResult, HistoryRecord
import uuid
import base64
import cv2
import numpy as np

# Simulación de base de datos en memoria (en producción usa una DB real)
history_db = []

async def save_to_history(detections: List[DetectionResult], image: Optional[bytes] = None) -> List[HistoryRecord]:
    """
    Guarda las detecciones en el historial y devuelve los registros recientes
    """
    global history_db
    
    new_records = []
    
    for detection in detections:
        # Convertir imagen a base64 si está disponible
        img_snapshot = None
        if image is not None:
            nparr = np.frombuffer(image, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            _, buffer = cv2.imencode('.jpg', img)
            img_snapshot = f"data:image/jpeg;base64,{base64.b64encode(buffer).decode('utf-8')}"
        
        record = HistoryRecord(
            id=str(uuid.uuid4()),
            timestamp=detection.timestamp,
            dominantEmotion=detection.dominantEmotion,
            emotions=detection.emotions,
            imageSnapshot=img_snapshot or ""
        )
        
        history_db.append(record)
        new_records.append(record)
    
    # Mantener solo los últimos 100 registros
    history_db = history_db[-100:]
    
    return new_records

async def get_history(limit: int = 10) -> List[HistoryRecord]:
    """
    Obtiene el historial reciente
    """
    return history_db[-limit:]

async def clear_history():
    """
    Limpia el historial
    """
    global history_db
    history_db = []