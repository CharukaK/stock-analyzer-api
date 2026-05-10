from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import get_symbol_service
from app.services.symbol import SymbolService


router = APIRouter()


@router.get("/symbols/{symbol}/annual/{year}")
async def symbols(
    symbol: str,
    year: int,
    symbolService: Annotated[SymbolService, Depends(get_symbol_service)],
):
    return await symbolService.get_symbol_data_annual(symbol, year)
