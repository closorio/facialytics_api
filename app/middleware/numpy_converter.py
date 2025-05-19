import numpy as np
from fastapi import Request
from fastapi.responses import JSONResponse
import json

def convert_numpy(obj):
    """Función recursiva para convertir tipos NumPy"""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_numpy(x) for x in obj]
    else:
        return obj

async def numpy_converter_middleware(request: Request, call_next):
    response = await call_next(request)
    
    try:
        # Solo procesar respuestas JSON exitosas
        if response.status_code == 200 and hasattr(response, "body"):
            response_body = json.loads(response.body.decode())
            converted_body = convert_numpy(response_body)
            return JSONResponse(converted_body)
    except Exception as e:
        print(f"Error en middleware: {str(e)}")
    
    return response