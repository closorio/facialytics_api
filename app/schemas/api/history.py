## @file: app/schemas/api/history.py

from datetime import datetime
from pydantic import BaseModel
from typing import List
from ..domain.emotions import EmotionScores

class HistoryRecord(BaseModel):
    id: str
    timestamp: datetime
    dominantEmotion: str
    emotions: EmotionScores
    imageSnapshot: str  # base64

class HistoryResponse(BaseModel):
    records: List[HistoryRecord]
    total: int  # Para paginación