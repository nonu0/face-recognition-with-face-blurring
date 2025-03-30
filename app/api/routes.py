import os 
import sys
import concurrent.futures 
from fastapi import APIRouter,HTTPException
from fastapi.responses import StreamingResponse,JSONResponse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.video_stream import start_streaming
import cv2
from utils.video_processing import CustomVideoCapture

router = APIRouter()
executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

@router.get("/video/{source:path}")
def video_stream(source: str):
    return executor.submit(start_streaming, source, True).result()