# app/schemas/api/video_processing.py
from pydantic import BaseModel
from typing import List, Dict
import numpy as np

class ProcessResponse(BaseModel):
    faces: List[Dict]
    frame_size: Dict[str, int]
    success: bool
    
    class Config:
        json_encoders = {
            np.integer: int,
            np.floating: float,
            np.ndarray: lambda x: x.tolist(),
            np.bool_: bool
        }
        
        @staticmethod
        def schema_extra(schema: Dict, model) -> None:
            for prop in schema.get('properties', {}).values():
                prop.pop('title', None)