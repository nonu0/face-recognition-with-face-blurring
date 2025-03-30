from fastapi import FastAPI
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import config


from app.api.routes import router


app = FastAPI(title=config.APP_NAME,version=config.VERSION)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8000)

