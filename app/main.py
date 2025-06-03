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
origins = [
    "http://localhost",
    "http://localhost:5500",
    "http://127.0.0.1",
    "http://127.0.0.1:5500",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://8j8j3stk-5173.use.devtunnels.ms",    
    # Añade aquí otros orígenes si es necesario
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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