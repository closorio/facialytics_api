# app/schemas/api/video_processing.py
from pydantic import BaseModel
from typing import List, Dict
from ..domain.faces import FaceDetectionResult

class ProcessResponse(BaseModel):
    faces: List[FaceDetectionResult]
    frame_size: Dict[str, int]
    success: bool