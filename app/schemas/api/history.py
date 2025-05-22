## @file: app/schemas/api/history.py

from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
from ..core import EmotionType, DetectionType
from ..domain.emotions import EmotionScores

class HistoryRecordBase(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    dominant_emotion: EmotionType
    emotion_scores: EmotionScores
    detection_type: DetectionType
    image_snapshot: str  # base64 encoded

class HistoryRecordCreate(HistoryRecordBase):
    pass

class HistoryRecord(HistoryRecordBase):
    id: str

class HistoryResponse(BaseModel):
    records: List[HistoryRecord]
    total: int
    page: Optional[int] = None
    per_page: Optional[int] = None