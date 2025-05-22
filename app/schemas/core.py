# app/schemas/core.py
from typing import Literal
from enum import Enum

EmotionType = Literal["anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"]
class DetectionType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"