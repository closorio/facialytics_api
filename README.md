# **Face Emotion Recognition**

## 📌 Descripción del Proyecto

Este proyecto implementa un sistema de **detección de emociones faciales en tiempo real** utilizando una cámara web. Combina técnicas avanzadas de visión por computadora con un modelo de aprendizaje profundo basado en la arquitectura ResNet50V2.

## ✨ Características Principales

- 🎭 Detección de **7 emociones básicas**:
  - Enojo (`angry`)
  - Disgusto (`disgust`)
  - Miedo (`fear`)
  - Felicidad (`happy`)
  - Neutral (`neutral`)
  - Tristeza (`sad`)
  - Sorpresa (`surprise`)

- 🖥️ **Interfaz en tiempo real** que muestra:
  - Caja delimitadora del rostro detectado
  - Emoción predicha con porcentaje de confianza
  - Indicador de FPS (cuadros por segundo)

- 🤖 **Modelo avanzado**:
  - Arquitectura ResNet50V2 optimizada
  - Modelo pre-entrenado en formato `.keras`
  - Procesamiento eficiente de imágenes

## 🛠️ Componentes Técnicos

- **Detección facial**: Usa OpenCV con un modelo Caffe pre-entrenado
- **Clasificación de emociones**: Modelo ResNet50V2 personalizado
- **Preprocesamiento**:
  - Normalización de imágenes (224x224 píxeles)
  - Conversión a espacio de color RGB
  - Escalado de valores de píxeles (0-1)

### Preparación del entorno
#### venv

    $ python3.10 -m venv venv

    Windows	.\venv\Scripts\activate
    Linux/macOS	source venv/bin/activate

    $ pip install -r requirements.txt 

#### Conda

    conda create -n face_emotion_env python=3.10 -y
    conda activate face_emotion_env

    $ pip install -r requirements.txt 

    
### Usando WebCam

Inicializar API

    $ uvicorn app.main:app --reload

API Docs
  http://127.0.0.1:8000/docs

API Stream 
  http://localhost:8000/api/v1/webcam/stream

API Process Last Frame
  http://localhost:8000/api/v1/webcam/process-latest-frame


