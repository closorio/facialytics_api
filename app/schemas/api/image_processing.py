# app/schemas/api/image_processing.py
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from ..domain.emotions import EmotionScores
from ..domain.faces import BoundingBox

class DetectionResult(BaseModel):
    faceId: str
    emotions: EmotionScores
    dominantEmotion: str  # Debería ser EmotionType pero hay discrepancia con el original
    timestamp: datetime
    boundingBox: BoundingBox

class HistoryRecord(BaseModel):
    id: str
    timestamp: datetime
    dominantEmotion: str
    emotions: EmotionScores
    imageSnapshot: str  # base64 encoded image

class DetectionResponse(BaseModel):
    detections: List[DetectionResult]
    history: List[HistoryRecord]