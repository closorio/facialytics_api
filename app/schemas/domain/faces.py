# app/schemas/domain/faces.py
from pydantic import BaseModel
from typing import Dict
from ..core import EmotionType

class BoundingBox(BaseModel):
    x: int  # esquina superior izquierda
    y: int
    width: int
    height: int

    # Método para convertir a tupla
    def to_tuple(self) -> tuple[int, int, int, int]:
        return (self.x, self.y, self.x + self.width, self.y + self.height)

class FaceDetectionResult(BaseModel):
    box: BoundingBox  # <-- Ahora usa la clase directamente
    scores: Dict[EmotionType, float]
    dominant_emotion: EmotionType