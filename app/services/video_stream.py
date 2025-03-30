from fastapi.responses import StreamingResponse
from utils.video_processing import CustomVideoCapture


def start_streaming(source:str,blur:bool=False):
    return StreamingResponse(CustomVideoCapture(source, blur).video_stream(), 
                             media_type="multipart/x-mixed-replace; boundary=frame")