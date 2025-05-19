from pydantic import BaseModel
from typing import Dict, List, Literal, Tuple


EmotionType = Literal["anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"]

class FaceResult(BaseModel):
    box: Tuple[int, int, int, int]  # (x1, y1, x2, y2)
    scores: Dict[EmotionType, float]
    dominant_emotion: EmotionType

class ProcessResponse(BaseModel):
    faces: List[FaceResult]
    frame_size: Dict[str, int]
    success: bool