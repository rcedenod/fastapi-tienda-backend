from fastapi import FastAPI
from routes import app_router
import uvicorn

app = FastAPI()

app.include_router(app_router)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, port=5000, host='0.0.0.0')
