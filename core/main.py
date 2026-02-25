from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from blog.routes import router as blog_router
from user.routes import router as user_router

app = FastAPI()

app.include_router(blog_router)
app.include_router(user_router)


@app.exception_handler(StarletteHTTPException)
def http_exception_handler(request, exc):
    error_response = {
        "error": True,
        "status_code": exc.status_code,
        "detail": str(exc.detail),
    }
    return JSONResponse(content=error_response, status_code=exc.status_code)
