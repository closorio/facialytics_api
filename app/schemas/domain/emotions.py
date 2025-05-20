# app/schemas/domain/emotions.py
from pydantic import BaseModel
from ..core import EmotionType

class EmotionScores(BaseModel):
    joy: float
    sadness: float
    anger: float
    surprise: float
    fear: float
    disgust: float
    neutral: float