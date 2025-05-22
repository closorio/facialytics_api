## @file: app/schemas/api/image_processing.py
from pydantic import BaseModel
from typing import List, Dict
import numpy as np
from ..domain.emotions import EmotionScores
from ..domain.faces import BoundingBox

class DetectionResult(BaseModel):
    faceId: str
    emotions: EmotionScores
    dominantEmotion: str
    timestamp: str
    boundingBox: BoundingBox

class DetectionResponse(BaseModel):
    detections: List[DetectionResult]
    frameInfo: Dict[str, int]
    
    class Config:
        json_encoders = {
            np.integer: int,
            np.floating: float,
            np.ndarray: lambda x: x.tolist(),
            np.bool_: bool
        }