from typing import Annotated
import aiosqlite
from fastapi import Depends, Request
from app.clients import AlphaVantageClient
from app.db.repositories import SymbolsRepository
from app.db.repositories.prices import PricesRepository
from app.services.symbol import SymbolService


def get_alphavantage_client(request: Request) -> AlphaVantageClient:
    return request.app.state.alphavantage_client


def get_db_conn(request: Request) -> aiosqlite.Connection:
    return request.app.state.db_conn


def get_symbol_service(
    av_client: Annotated[AlphaVantageClient, Depends(get_alphavantage_client)],
    db_conn: Annotated[aiosqlite.Connection, Depends(get_db_conn)],
) -> SymbolService:
    return SymbolService(av_client, SymbolsRepository(db_conn), PricesRepository(db_conn))
