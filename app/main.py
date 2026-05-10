from fastapi import FastAPI
from app.clients import AlphaVantageClient
from app.db import open_db
from app.routes import health_router, symbols_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.alphavantage_client = AlphaVantageClient()
    app.state.db_conn = await open_db()
    yield
    await app.state.alphavantage_client.aclose()
    await app.state.db_conn.close()


app = FastAPI(lifespan=lifespan)

app.include_router(health_router)
app.include_router(symbols_router)
