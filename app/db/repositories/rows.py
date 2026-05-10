from pydantic import BaseModel


class SymbolRow(BaseModel):
    information: str
    symbol: str
    last_refreshed: str
    time_zone: str


class PriceRow(BaseModel):
    symbol: str
    month_start_date: str
    last_refreshed: str
    open: float
    high: float
    low: float
    close: float
    volume: int
