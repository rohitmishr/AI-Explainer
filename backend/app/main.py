from app.app import app
from app.routes import router
from fastapi.staticfiles import StaticFiles

app.include_router(router)

app.mount("/static", StaticFiles(directory="static"), name="static")
