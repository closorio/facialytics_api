## @file app/services/video_processing_service.py

import cv2
import threading
import time 
import base64
from datetime import datetime
import numpy as np
import logging
from app.schemas.core import DetectionType
from app.schemas.api.history import HistoryRecordCreate
from app.services.history_repository import history_repo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WebcamService")

class WebcamService:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None
        self.latest_frame = np.zeros((480, 640, 3), dtype=np.uint8)  # Frame negro por defecto
        self.running = False
        self.lock = threading.Lock()
        self._init_camera()

    def _init_camera(self):
        """Intenta inicializar con diferentes backends"""
        backends = [
            cv2.CAP_V4L2,  # Linux
            cv2.CAP_DSHOW,  # Windows
            cv2.CAP_ANY     # Intento genérico
        ]
        
        for backend in backends:
            try:
                self.cap = cv2.VideoCapture(self.camera_index, backend)
                if self.cap.isOpened():
                    logger.info(f"Cámara inicializada con backend: {backend}")
                    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                    return
            except Exception as e:
                logger.warning(f"Error con backend {backend}: {str(e)}")
        
        logger.error("No se pudo inicializar la cámara real. Usando simulador.")
        self._init_simulator()

    def _init_simulator(self):
        """Inicializa un generador de frames de prueba"""
        self.simulator_mode = True
        self.test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(self.test_frame, "MODO SIMULADOR", (50, 240), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._update_frame, daemon=True)
            self.thread.start()
            logger.info("Servicio de cámara iniciado")

    def _update_frame(self):
        frame_count = 0
        while self.running:
            if hasattr(self, 'simulator_mode'):
                with self.lock:
                    self.latest_frame = self.test_frame.copy()
                    cv2.putText(self.latest_frame, f"Frame: {frame_count}", (50, 280),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                frame_count += 1
            else:
                ret, frame = self.cap.read()
                if ret:
                    with self.lock:
                        self.latest_frame = frame
                else:
                    logger.warning("Error leyendo frame de cámara")
            time.sleep(0.033)  # ~30 FPS

    def get_latest_frame(self) -> np.ndarray:
        with self.lock:
            return self.latest_frame.copy()

    def stop(self):
        self.running = False
        if hasattr(self, 'thread'):
            self.thread.join()
        if hasattr(self, 'cap') and self.cap:
            self.cap.release()
        logger.info("Servicio de cámara detenido")
        

    async def process_frame(self, emotion_model) -> dict:
        frame = self.get_latest_frame()
        if frame is None:
            raise ValueError("No frame available")
        
        raw_faces = emotion_model.predict_emotion(frame)
        
        if raw_faces:
            try:
                # Procesar la cara dominante
                dominant_face = max(raw_faces, key=lambda x: max(x["scores"].values()))
                
                # Crear registro de historial
                record_data = HistoryRecordCreate(
                    timestamp=datetime.utcnow(),
                    dominant_emotion=dominant_face["dominant_emotion"],
                    emotion_scores={
                        "joy": float(dominant_face["scores"].get("joy", 0)),
                        "sadness": float(dominant_face["scores"].get("sadness", 0)),
                        "anger": float(dominant_face["scores"].get("anger", 0)),
                        "surprise": float(dominant_face["scores"].get("surprise", 0)),
                        "fear": float(dominant_face["scores"].get("fear", 0)),
                        "disgust": float(dominant_face["scores"].get("disgust", 0)),
                        "neutral": float(dominant_face["scores"].get("neutral", 0))
                    },
                    detection_type=DetectionType.VIDEO,
                    image_snapshot=self._frame_to_base64(frame)
                )
                
                await history_repo.create_record(record_data)

            except Exception as e:
                logger.error(f"Error al guardar en historial: {str(e)}")
                
        # Convertir todos los valores NumPy a nativos
        processed_faces = []
        for face in raw_faces:
            processed_face = {
                "box": {
                    "x": int(face["box"]["x"]),
                    "y": int(face["box"]["y"]),
                    "width": int(face["box"]["width"]),
                    "height": int(face["box"]["height"])
                },
                "scores": {k: float(v) for k, v in face["scores"].items()},
                "dominant_emotion": str(face["dominant_emotion"])
            }
            processed_faces.append(processed_face)
        
        return {
            "faces": processed_faces,
            "frame_size": {
                "height": int(frame.shape[0]),
                "width": int(frame.shape[1]),
                "channels": int(frame.shape[2]) if len(frame.shape) > 2 else 1
            },
            "success": True
        }
    
    def _frame_to_base64(self, frame: np.ndarray) -> str:
        """Convierte un frame de video a base64"""
        try:
            _, buffer = cv2.imencode('.jpg', frame)
            return f"data:image/jpeg;base64,{base64.b64encode(buffer).decode('utf-8')}"
        except Exception as e:
            logger.error(f"Error al convertir frame a base64: {str(e)}")
            return ""