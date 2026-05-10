import aiosqlite
from datetime import date

from app.db.repositories import PriceRow
from app.models.alphavantage import MonthlyDataPoint


class PricesRepository:
    def __init__(self, conn: aiosqlite.Connection) -> None:
        self._conn: aiosqlite.Connection = conn

    async def get_annual(self, symbol: str, year: int) -> list[PriceRow] | None:
        async with self._conn.execute(
            """
                SELECT symbol, month_start_date, last_refreshed, open, close, high, low, volume
                FROM prices_monthly WHERE symbol = ? AND strftime('%Y', month_start_date) = ?
            """,
            (symbol, year),
        ) as cursor:
            rows = await cursor.fetchall()
            return [PriceRow(**dict(row)) for row in rows]

    async def upsert_monthly(
        self, symbol: str, data: dict[str, MonthlyDataPoint], last_refreshed: str
    ):
        rows = [
            (
                symbol,
                _to_month_start(date_str),
                last_refreshed,
                point.open,
                point.close,
                point.high,
                point.low,
                point.volume,
            )
            for date_str, point in data.items()
        ]
        await self._conn.executemany(
            """
                INSERT INTO prices_monthly
                    (symbol, month_start_date, last_refreshed, open, close, high, low, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(symbol, month_start_date) DO UPDATE SET
                    last_refreshed = excluded.last_refreshed,
                    open           = excluded.open,
                    close          = excluded.close,
                    high           = excluded.high,
                    low            = excluded.low,
                    volume         = excluded.volume
            """,
            rows,
        )
        await self._conn.commit()


def _to_month_start(date_str: str) -> str:
    """Convert date string to the first day of its month: '2026-04-30' → '2026-04-01'"""
    d = date.fromisoformat(date_str)
    return d.replace(day=1).isoformat()
