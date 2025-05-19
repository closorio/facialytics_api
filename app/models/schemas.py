from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime

class BoundingBox(BaseModel):
    x: int
    y: int
    width: int
    height: int

class EmotionScores(BaseModel):
    joy: float
    sadness: float
    anger: float
    surprise: float
    fear: float
    disgust: float
    neutral: float

class DetectionResult(BaseModel):
    faceId: str
    emotions: EmotionScores
    dominantEmotion: str
    timestamp: datetime
    boundingBox: BoundingBox

class HistoryRecord(BaseModel):
    id: str
    timestamp: datetime
    dominantEmotion: str
    emotions: EmotionScores
    imageSnapshot: str

class DetectionResponse(BaseModel):
    detections: List[DetectionResult]
    history: List[HistoryRecord]

class ImageData(BaseModel):
    image: str  # base64 encoded image