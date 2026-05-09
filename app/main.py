from fastapi import FastAPI
from app.clients import AlphaVantageClient
from app.routes import health_router, symbols_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.alphavantage_client = AlphaVantageClient()
    yield
    await app.state.alphavantage_client.aclose()


app = FastAPI(lifespan=lifespan)

app.include_router(health_router)
app.include_router(symbols_router)
