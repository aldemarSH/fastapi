# python -m virtualenv env
#.\env\Scripts\activate
# pip install fastAPI
# pip install "uvicorn[standard]"
# uvicorn main:app --reload
# para ejecutar requirements.txt ->  pip install -r requirements.txt

from fastapi import FastAPI
from router import blog_get, blog_post, user, article
from db.database import engine
from db import models




app = FastAPI()
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(user.router)
app.include_router(article.router)

@app.get('/hello')
def index():
    return {'mensaje': 'hola mundo'}

# @app.get('/blog/all')
# def get_all_blogs():
#     return {'mensaje': 'todos los blogs fueron entregados'}

models.Base.metadata.create_all(engine)

