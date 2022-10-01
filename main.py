from fastapi import FastAPI
from db.models import Category
from db.database import session
from routes import category, video, user
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI()


app.include_router(category.router)
app.include_router(video.router)
app.include_router(user.router)


origins = [
    'http://localhost:3000'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)


if __name__ == '__main__':
    uvicorn.run(app,host='0.0.0.0', port=8000)
