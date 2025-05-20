## @file app/services/image_processing_service.py

from datetime import datetime
import uuid
import cv2
import numpy as np
from app.schemas.api.image_processing import DetectionResult, DetectionResponse
from app.schemas.domain.emotions import EmotionScores
from app.schemas.domain.faces import BoundingBox  # Para la clase
from app.services.history_repository import save_to_history

async def process_image(image, emotion_model):
    # Convertir imagen a formato OpenCV
    nparr = np.frombuffer(image, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if frame is None:
        raise ValueError("No se pudo decodificar la imagen")
    
    # Detectar emociones
    faces = emotion_model.predict_emotion(frame)
    
    detections = []
    
    for face in faces:
        # Asegúrate de convertir los valores a enteros
        box = face["box"]
        x = int(box["x"])
        y = int(box["y"])
        width = int(box["width"])
        height = int(box["height"])
        
        detection = DetectionResult(
            faceId=f"face-{str(uuid.uuid4())[:8]}",
            emotions=EmotionScores(**face["scores"]),
            dominantEmotion=face["dominant_emotion"],
            timestamp=datetime.utcnow(),
            boundingBox=BoundingBox(
                x=x,
                y=y,
                width=width,
                height=height
            )
        )
        detections.append(detection)
    
    # Guardar en historial
    history = await save_to_history(detections, image)
    
    return DetectionResponse(detections=detections, history=history)