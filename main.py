# category, video

from fastapi import FastAPI
from routers import category
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(category.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods = ['*'],
    allow_headers = ['*'] 
)


@app.get('/hello')
def index():
    return {'message': 'hola mundo'}