# **Face Emotion Recognition**

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/closorio/facialytics_api)
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
  - Transfer Learning en los pesos de aprendizaje con `imagenet` de AffectNet
  - Modelo entrenado en formato `.keras`
  - Procesamiento eficiente de con generador de imágenes

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

    
## Usando WebCam

### Inicializar API

    $ uvicorn app.main:app --reload

### API Docs
    http://localhost:8000/docs

### API Process Image (Probar desde docs)
    http://localhost:8000/api/v1/detection/process-image    

### API Process Lastest Frame
    http://localhost:8000/api/v1/webcam/process-frame

### API History
    http://localhost:8000/api/v1/history/
    http://localhost:8000/api/v1/history/?page=1&per_page=10&detection_type=image
    http://localhost:8000/api/v1/history/?page=1&per_page=10&detection_type=video


## Configuraciones de Docker
### Para crear build:
  docker build -t emotion-detection-api .

### Para iniciar contenedor docker
  docker run -p 8000:8000 emotion-detection-api


### Repositorio Docker Hub
  docker login
  docker tag emotion-detection-api closorio/emotion-detection-api:1.0
  docker push closorio/emotion-detection-api:1.0

#### Cada 10 imágenes consumen aproximadamente 1.7 GBs de RAM