import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.clients import AlphaVantageClient
from app.core import settings
from app.db import open_db
from app.exceptions import ExternalAPIError, SymbolNotFoundError
from app.exceptions.exceptions import DataBaseError
from app.routes import health_router, symbols_router
from contextlib import asynccontextmanager

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.alphavantage_client = AlphaVantageClient()
    app.state.db_conn = await open_db()
    yield
    await app.state.alphavantage_client.aclose()
    await app.state.db_conn.close()


app = FastAPI(lifespan=lifespan)


@app.exception_handler(SymbolNotFoundError)
async def symbol_not_found_handler(_: Request, exc: SymbolNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(ExternalAPIError)
async def external_api_error_handler(_: Request, exc: ExternalAPIError):
    return JSONResponse(status_code=503, content={"detail": str(exc)})


@app.exception_handler(Exception)
async def database_error_handler(_: Request, exc: DataBaseError):
    return JSONResponse(status_code=500, content={"detail": str(exc)})


@app.exception_handler(Exception)
async def generic_error_handler(_: Request, exc: Exception):
    logger.error("Unhandled exception: %s", exc, exc_info=True)
    return JSONResponse(
        status_code=500, content={"detail": "An unexpected error occurred"}
    )


app.include_router(health_router)
app.include_router(symbols_router)
