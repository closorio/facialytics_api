import cv2
import threading
import time
import numpy as np
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WebcamService")

class WebcamService:
    def __init__(self, camera_index=1):
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