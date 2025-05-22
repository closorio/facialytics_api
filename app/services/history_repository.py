## @file: app/services/history_repository.py

from typing import List, Optional
import uuid
import base64
import cv2
import logging
from typing import Optional
import numpy as np
from app.schemas.api.history import HistoryRecord, HistoryRecordCreate

logger = logging.getLogger(__name__)

class HistoryRepository:
    def __init__(self):
        self._history: List[HistoryRecord] = []
        self._max_records = 100

    async def create_record(self, record_data: HistoryRecordCreate) -> HistoryRecord:
        try:
            logger.info(f"Intentando crear registro: {record_data.dict()}")
            record = HistoryRecord(
                id=str(uuid.uuid4()),
                **record_data.dict()
            )
            self._history.append(record)
            
            if len(self._history) > self._max_records:
                self._history = self._history[-self._max_records:]
                
            logger.info(f"Registro creado exitosamente. Total: {len(self._history)}")
            return record
        except Exception as e:
            logger.error(f"Error al crear registro: {str(e)}")
            raise

    async def get_history(
        self, 
        page: Optional[int] = None, 
        per_page: Optional[int] = 10,
        detection_type: Optional[str] = None
    ) -> List[HistoryRecord]:
        """Obtiene el historial con paginación y filtrado por tipo"""
        try:
            # Filtrar por tipo si se especifica
            filtered_records = [
                record for record in self._history
                if detection_type is None or record.detection_type.lower() == detection_type.lower()
            ][::-1]  # Más recientes primero
            
            # Aplicar paginación
            if page is not None and per_page is not None:
                start = (page - 1) * per_page
                end = start + per_page
                return filtered_records[start:end]
                
            return filtered_records
        except Exception as e:
            logger.error(f"Error al obtener historial: {str(e)}")
            raise

    async def clear_history(self) -> None:
        """Borra todo el historial"""
        self._history = []

    @staticmethod
    def image_to_base64(image: np.ndarray) -> str:
        """Convierte una imagen OpenCV a base64"""
        _, buffer = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 70])
        return f"data:image/jpeg;base64,{base64.b64encode(buffer).decode('utf-8')}"

# Instancia singleton
history_repo = HistoryRepository()