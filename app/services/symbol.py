import logging
import sys
from datetime import datetime, timedelta, timezone
from app.clients import AlphaVantageClient
from app.db.repositories import SymbolsRepository, PricesRepository
from app.models.responses import AnnualSummaryResponse

logger = logging.getLogger()

class SymbolService:
    def __init__(
        self,
        av_client: AlphaVantageClient,
        symbol_repository: SymbolsRepository,
        prices_repository: PricesRepository,
    ) -> None:
        self._av_client: AlphaVantageClient = av_client
        self._symbol_repository: SymbolsRepository = symbol_repository
        self._prices_repository: PricesRepository = prices_repository

    async def get_symbol_data_annual(
        self, symbol: str, year: int
    ) -> AnnualSummaryResponse | None:
        logger.info("recieved request for %s year=%s", symbol, year)
        current_year = datetime.now(timezone.utc).year
        is_current_year = year == current_year

        symbol_metadata = await self._symbol_repository.get(symbol)

        logger.debug("symbol_metadata = %s", symbol_metadata)
        
        if symbol_metadata is None:
            # fetch data
            await self._fetch_and_store_data(symbol)
        elif is_current_year:
            is_cache_stale = datetime.now(timezone.utc) - datetime.fromisoformat(
                symbol_metadata.last_refreshed
            ).replace(tzinfo=timezone.utc) > timedelta(days=1)

            if is_cache_stale:
                await self._fetch_and_store_data(symbol)

        return await self._aggregate_monthly(symbol, year)

    async def _fetch_and_store_data(self, symbol: str):
        response = await self._av_client.get_monthly_price_data(symbol)
        await self._symbol_repository.upsert(symbol, response.metadata)
        await self._prices_repository.upsert_monthly(
            symbol,
            response.monthly_time_series,
            response.metadata.last_refreshed.isoformat(),
        )

    async def _aggregate_monthly(
        self, symbol: str, year: int
    ) -> AnnualSummaryResponse | None:
        rows = await self._prices_repository.get_annual(symbol, year)
        if not rows:
            return None
        high: float = sys.float_info.min
        low: float = sys.float_info.max
        volume: int = 0
        for row in rows:
            high = max(high, row.high)
            low = min(low, row.low)
            volume += row.volume

        return AnnualSummaryResponse(high=high, low=low, volume=volume)
