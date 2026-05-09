from fastapi import FastAPI

from app.routes import health_router, symbols_router

app = FastAPI()

app.include_router(health_router)
app.include_router(symbols_router)

