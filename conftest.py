from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock
import pytest
from app.clients import AlphaVantageClient
from app.db.repositories import SymbolsRepository, PricesRepository
from app.db.repositories.rows import SymbolRow, PriceRow
from app.services.symbol import SymbolService


def _iso(dt: datetime) -> str:
    return dt.isoformat()


@pytest.fixture
def mock_av_client() -> AsyncMock:
    return AsyncMock(spec=AlphaVantageClient)


@pytest.fixture
def mock_symbol_repo() -> AsyncMock:
    return AsyncMock(spec=SymbolsRepository)


@pytest.fixture
def mock_prices_repo() -> AsyncMock:
    return AsyncMock(spec=PricesRepository)


@pytest.fixture
def symbol_service(
    mock_av_client: AsyncMock,
    mock_symbol_repo: AsyncMock,
    mock_prices_repo: AsyncMock,
) -> SymbolService:
    return SymbolService(mock_av_client, mock_symbol_repo, mock_prices_repo)


@pytest.fixture
def fresh_symbol_row() -> SymbolRow:
    """last_refreshed is within the last hour — cache is fresh."""
    return SymbolRow(
        symbol="IBM",
        last_refreshed=_iso(datetime.now(timezone.utc)),
        last_checked=_iso(datetime.now(timezone.utc)),
        time_zone="US/Eastern",
    )


@pytest.fixture
def stale_symbol_row() -> SymbolRow:
    """last_refreshed is 2 days ago — cache is stale."""
    return SymbolRow(
        symbol="IBM",
        last_checked=_iso(datetime.now(timezone.utc) - timedelta(days=2)),
        last_refreshed=_iso(datetime.now(timezone.utc) - timedelta(days=2)),
        time_zone="US/Eastern",
    )


@pytest.fixture
def sample_price_rows() -> list[PriceRow]:
    return [
        PriceRow(
            symbol="IBM",
            month_start_date="2024-01-01",
            last_refreshed="2024-01-31",
            open=140.0,
            high=160.0,
            low=130.0,
            close=155.0,
            volume=1_000_000,
        ),
        PriceRow(
            symbol="IBM",
            month_start_date="2024-02-01",
            last_refreshed="2024-02-29",
            open=155.0,
            high=170.0,
            low=145.0,
            close=165.0,
            volume=900_000,
        ),
    ]
