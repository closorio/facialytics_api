import cv2
import numpy as np
from tensorflow.keras.models import load_model  # type: ignore
from tensorflow.keras.utils import img_to_array  # type: ignore
import threading
from typing import Dict, List, Tuple

class EmotionModel:
    _lock = threading.Lock()  # Lock para operaciones que no son thread-safe
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        """Implementación singleton thread-safe"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(EmotionModel, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, model_path: str = "models/RESNET50/emotion_recognition_resnet50v2.keras"):
        """Inicialización thread-safe con doble verificación"""
        if self._initialized:
            return
            
        with self._lock:
            if not self._initialized:
                # Cargar modelo de emociones (solo una vez)
                self.emotion_model = load_model(model_path)
                self.classes = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
                
                # Cargar modelo de detección de rostros
                self.prototxt_path = "face_detector/deploy.prototxt"
                self.weights_path = "face_detector/res10_300x300_ssd_iter_140000.caffemodel"
                self.face_net = cv2.dnn.readNet(self.prototxt_path, self.weights_path)
                
                # Marcar como inicializado
                self._initialized = True
    
    def detect_faces(self, frame: np.ndarray) -> Tuple[np.ndarray, int, int]:
        """
        Detecta rostros en un frame de imagen.
        Thread-safe: solo usa variables locales y de instancia de solo lectura.
        """
        (h, w) = frame.shape[:2]
        
        # BlobFromImage y forward necesitan lock por usar recursos compartidos de OpenCV
        with self._lock:
            blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
            self.face_net.setInput(blob)
            detections = self.face_net.forward()
        
        return detections, h, w
    
    def predict_emotion(self, frame: np.ndarray) -> List[Dict]:
        """
        Predice emociones en los rostros detectados.
        Thread-safe: operaciones independientes con locking donde es necesario.
        """
        # Detectar rostros (ya maneja su propio locking)
        detections, h, w = self.detect_faces(frame)
        
        faces = []
        
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            
            if confidence > 0.4:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (Xi, Yi, Xf, Yf) = box.astype("int")

                Xi, Yi = max(0, Xi), max(0, Yi)
                Xf, Yf = min(w - 1, Xf), min(h - 1, Yf)
                
                face = frame[Yi:Yf, Xi:Xf]
                if face.size == 0:
                    continue
                    
                # Preprocesamiento (operaciones thread-safe de OpenCV/NumPy)
                face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                face = cv2.resize(face, (224, 224))
                face = img_to_array(face)
                face = np.expand_dims(face, axis=0)
                face = face / 255.0

                # Predecir emociones (necesita lock para Keras)
                with self._lock:
                    pred = self.emotion_model.predict(face, verbose=0)[0]
                
                # Procesamiento posterior (thread-safe)
                emotion_mapping = {
                    'angry': 'anger',
                    'disgust': 'disgust',
                    'fear': 'fear',
                    'happy': 'joy',
                    'neutral': 'neutral',
                    'sad': 'sadness',
                    'surprise': 'surprise'
                }
                
                emotion_scores = {
                    emotion_mapping[self.classes[i]]: float(pred[i]) 
                    for i in range(len(self.classes))
                }
                
                # Normalizar scores
                total = sum(emotion_scores.values())
                normalized_scores = {k: v/total for k, v in emotion_scores.items()}
                
                # Emoción dominante
                dominant_idx = np.argmax(pred)
                dominant_emotion = emotion_mapping[self.classes[dominant_idx]]
                
                faces.append({
                    "box": {
                        "x": Xi,
                        "y": Yi,
                        "width": Xf - Xi,
                        "height": Yf - Yi
                    },
                    "scores": normalized_scores,
                    "dominant_emotion": dominant_emotion
                })
        
        return faces