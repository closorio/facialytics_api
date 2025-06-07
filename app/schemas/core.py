# app/schemas/core.py
from typing import Literal
from enum import Enum

EmotionType = Literal["anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"]
class DetectionType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"

class DominantEmotion(str, Enum):
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    SURPRISE = "surprise"
    FEAR = "fear"
    DISGUST = "disgust"
    NEUTRAL = "neutral"