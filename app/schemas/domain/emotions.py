# app/schemas/domain/emotions.py
from pydantic import BaseModel
from ..core import EmotionType

class EmotionScores(BaseModel):
    joy: float = 0.0
    sadness: float = 0.0
    anger: float = 0.0
    surprise: float = 0.0
    fear: float = 0.0
    disgust: float = 0.0
    neutral: float = 0.0