import aiosqlite
from app.core import settings


async def open_db() -> aiosqlite.Connection:
    conn = await aiosqlite.connect(settings.DATABASE_URL)
    conn.row_factory = aiosqlite.Row  # convert tuples to dicts
    _ = await conn.execute("PRAGMA foreign_keys = ON")
    return conn

