# app/middleware/serialization_middleware.py
import numpy as np
from fastapi import Request
from fastapi.responses import JSONResponse
import json
from typing import Any
import logging

logger = logging.getLogger(__name__)

def convert_numpy_types(obj: Any) -> Any:
    """Convierte recursivamente tipos NumPy a tipos nativos de Python"""
    if isinstance(obj, (np.integer, np.int8, np.int16, np.int32, np.int64,
                      np.uint8, np.uint16, np.uint32, np.uint64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float16, np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, dict):
        return {k: convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_numpy_types(item) for item in obj]
    elif hasattr(obj, '__dict__'):
        return convert_numpy_types(vars(obj))
    else:
        return obj

async def serialization_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        
        if not (200 <= response.status_code < 300):
            return response
            
        if not hasattr(response, 'body'):
            return response
            
        content_type = response.headers.get('content-type', '')
        if 'application/json' not in content_type:
            return response
            
        try:
            response_body = json.loads(response.body.decode('utf-8'))
            converted_body = convert_numpy_types(response_body)
            return JSONResponse(
                content=converted_body,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except json.JSONDecodeError:
            logger.warning("Response body is not valid JSON")
            return response
        except Exception as e:
            logger.error(f"Serialization error: {str(e)}", exc_info=True)
            return response
            
    except Exception as e:
        logger.error(f"Middleware error: {str(e)}", exc_info=True)
        raise