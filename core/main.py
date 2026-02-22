from fastapi import FastAPI
from blog.routes import router as blog_router
from user.router import router as user_router


app = FastAPI()

app.include_router(blog_router)
app.include_router(user_router)
