import logging
import sys
from datetime import datetime, timedelta, timezone

import aiosqlite
import httpx
from pydantic import ValidationError
from app.clients import AlphaVantageClient
from app.db.repositories import SymbolsRepository, PricesRepository
from app.exceptions import ExternalAPIError, SymbolNotFoundError
from app.exceptions.exceptions import DataBaseError
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
    ) -> AnnualSummaryResponse:
        logger.info("recieved request for %s year=%s", symbol, year)
        try:
            symbol_metadata = await self._symbol_repository.get(symbol)
        except aiosqlite.Error as e:
            logger.error("database error occured: %s", e)
            raise DataBaseError()

        logger.debug("symbol_metadata = %s", symbol_metadata)

        if symbol_metadata is None:
            await self._fetch_and_store_data(symbol)
        else:
            last_cheked_year = datetime.fromisoformat(symbol_metadata.last_checked).year
            # only need to consider fetching if the last_cheked_year is less than or equal to current
            if year >= last_cheked_year:
                # api data is updated once a day so last_checked is enough to determine staleness
                is_cache_stale = symbol_metadata.last_checked != datetime.now(
                    timezone.utc
                ).strftime("%Y-%m-%d")

                if is_cache_stale:
                    await self._fetch_and_store_data(symbol)

        return await self._aggregate_monthly(symbol, year)

    async def _fetch_and_store_data(self, symbol: str):
        try:
            response = await self._av_client.get_monthly_price_data(symbol)
        except (httpx.HTTPStatusError, httpx.RequestError, ValidationError) as e:
            logger.error("data sourcing failed for %s: %s", symbol, e)
            raise ExternalAPIError()
        try:
            await self._symbol_repository.upsert(
                symbol,
                response.metadata,
                datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            )
            await self._prices_repository.upsert_monthly(
                symbol,
                response.monthly_time_series,
                response.metadata.last_refreshed.isoformat(),
            )
        except aiosqlite.Error as e:
            logger.error("database error occured: %s", e)
            raise DataBaseError()

    async def _aggregate_monthly(self, symbol: str, year: int) -> AnnualSummaryResponse:
        try:
            rows = await self._prices_repository.get_annual(symbol, year)
        except aiosqlite.Error as e:
            logger.error("database error occured: %s", e)
            raise DataBaseError()

        if not rows:
            raise SymbolNotFoundError(symbol, year)
        high: float = sys.float_info.min
        low: float = sys.float_info.max
        volume: int = 0
        for row in rows:
            high = max(high, row.high)
            low = min(low, row.low)
            volume += row.volume

        return AnnualSummaryResponse(high=high, low=low, volume=volume)
