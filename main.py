# category, video

from fastapi import FastAPI
from routers import category, video
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(category.router)
app.include_router(video.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods = ['*'],
    allow_headers = ['*'] 
)


@app.get('/healthcheck')
def index():
    return {'message': 'is working'}