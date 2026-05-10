import aiosqlite

from app.db.repositories.rows import SymbolRow
from app.models.alphavantage import MetaData


class SymbolsRepository:
    def __init__(self, conn: aiosqlite.Connection) -> None:
        self._conn: aiosqlite.Connection = conn

    async def get(self, symbol: str) -> SymbolRow | None:
        async with self._conn.execute(
            """
                SELECT symbol, last_refreshed, time_zone, last_checked
                FROM symbols WHERE symbol = ?
            """,
            (symbol,),
        ) as cursor:
            row = await cursor.fetchone()
            if row is None:
                return None
            return SymbolRow(**dict(row))

    async def upsert(self, symbol: str, metadata: MetaData, last_checked: str):
        await self._conn.execute(
            """
                INSERT INTO symbols (symbol, last_refreshed, time_zone, last_checked)
                VALUES (?,?,?,?)
                ON CONFLICT(symbol) DO UPDATE SET
                   last_refreshed = excluded.last_refreshed,
                   time_zone = excluded.time_zone,
                   last_checked = excluded.last_checked
            """,
            (
                metadata.symbol,
                metadata.last_refreshed,
                metadata.time_zone,
                last_checked,
            ),
        )
        await self._conn.commit()
