## @file app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import history_router, image_processing_router, video_processing_router
from app.middleware.serialization_middleware import serialization_middleware

app = FastAPI(
    title="Emotion Detection API",
    description="API for real-time emotion detection using RESNET50V2 model",
    version="1.0.0"
)

# Middleware to convert NumPy types to native Python types
app.middleware("http")(serialization_middleware)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajustar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(image_processing_router.router, prefix="/api/v1/detection", tags=["detection"])
app.include_router(history_router.router, prefix="/api/v1/history", tags=["history"])
app.include_router(video_processing_router.router, prefix="/api/v1/webcam", tags=["webcam"])

@app.get("/")
async def root():
    return {"message": "Emotion Detection API"}

@app.on_event("startup")
async def startup_event():
    # Puedes inicializar recursos costosos aquí
    pass

@app.on_event("shutdown")
async def shutdown_event():
    # Limpieza de recursos
    pass