import aiosqlite

from app.db.repositories.rows import SymbolRow
from app.models.alphavantage import MetaData


class SymbolsRepository:
    def __init__(self, conn: aiosqlite.Connection) -> None:
        self._conn: aiosqlite.Connection = conn

    async def get(self, symbol: str) -> SymbolRow | None:
        async with self._conn.execute(
            "SELECT symbol, info, last_refreshed, timezone",
            "FROM symbols WHERE symbol = ?",
            (symbol),
        ) as cursor:
            row = await cursor.fetchone()
            if row is None:
                return None
            return SymbolRow(**dict(row))

    async def upsert(self, symbol: str, metadata: MetaData):
        await self._conn.execute(
            "INSERT INTO symbols (symbol, information, last_refreshed, timezone)",
            "VALUES (?,?,?,?)",
            "ON CONFLICT(symbol) DO UPDATE SET",
            "   information = excluded.information",
            "   last_refreshed = excluded.last_refreshed",
            "   timezone = excluded.timezone",
            (
                metadata.symbol,
                metadata.information,
                metadata.last_refreshed,
                metadata.time_zone,
            ),
        )
        await self._conn.commit()
