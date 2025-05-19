from datetime import datetime
import uuid
import cv2
import numpy as np
from app.models.schemas import DetectionResult, EmotionScores, BoundingBox, DetectionResponse, HistoryRecord
from app.services.storage import save_to_history

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
        (Xi, Yi, Xf, Yf) = face["box"]
        
        detection = DetectionResult(
            faceId=f"face-{str(uuid.uuid4())[:8]}",
            emotions=EmotionScores(**face["scores"]),
            dominantEmotion=face["dominant_emotion"],
            timestamp=datetime.utcnow(),
            boundingBox=BoundingBox(
                x=Xi,
                y=Yi,
                width=Xf - Xi,
                height=Yf - Yi
            )
        )
        detections.append(detection)
    
    # Guardar en historial
    history = await save_to_history(detections, image)
    
    return DetectionResponse(detections=detections, history=history)