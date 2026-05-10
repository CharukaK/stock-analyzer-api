import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.db.repositories import PriceRow, SymbolRow, SymbolsRepository
from app.models.responses import AnnualSummaryResponse

HISTORICAL_YEAR = 2024
CURRENT_YEAR = datetime.datetime.now(datetime.timezone.utc).year


@pytest.mark.asyncio
async def test_returns_cached_data_for_historical_year(
    symbol_service: AsyncMock,
    mock_symbol_repo: AsyncMock,
    mock_prices_repo: AsyncMock,
    fresh_symbol_row: SymbolRow,
    sample_price_rows: list[PriceRow],
):
    mock_symbol_repo.get.return_value = fresh_symbol_row  # pyright: ignore[reportAny]
    mock_prices_repo.get_annual.return_value = sample_price_rows  # pyright: ignore[reportAny]

    result = await symbol_service.get_symbol_data_annual("IBM", HISTORICAL_YEAR)
    mock_symbol_repo.get.assert_awaited_once_with("IBM")  # pyright: ignore[reportAny]
    symbol_service._av_client.get_monthly_price_data.assert_not_awaited()  # pyright: ignore[reportAny]
    assert isinstance(result, AnnualSummaryResponse)
    assert result.high == "170.0000"
    assert result.low == "130.0000"  
    assert result.volume == "1900000"


@pytest.mark.asyncio
async def test_fetches_and_stores_when_symbol_not_in_db(
    symbol_service: AsyncMock,
    mock_symbol_repo: AsyncMock,
    mock_prices_repo: AsyncMock,
    sample_price_rows: list[PriceRow],
):
    mock_symbol_repo.get.return_value = None  # pyright: ignore[reportAny]
    mock_prices_repo.get_annual.return_value = sample_price_rows  # pyright: ignore[reportAny]
    av_response = MagicMock()
    av_response.metadata.last_refreshed.isoformat.return_value = "2024-01-31"  # pyright: ignore[reportAny]
    symbol_service._av_client.get_monthly_price_data.return_value = av_response  # pyright: ignore[reportAny]
    result = await symbol_service.get_symbol_data_annual("IBM", HISTORICAL_YEAR)  # pyright: ignore[reportAny]

    # verify that the API got called from function
    symbol_service._av_client.get_monthly_price_data.assert_awaited_once_with("IBM")  # pyright: ignore[reportAny]
    # verify the function tried to save metadata
    mock_symbol_repo.upsert.assert_awaited_once()  # pyright: ignore[reportAny]
    # verify the function tried to save price data
    mock_prices_repo.upsert_monthly.assert_awaited_once()  # pyright: ignore[reportAny]
    # verify return type
    assert isinstance(result, AnnualSummaryResponse)


