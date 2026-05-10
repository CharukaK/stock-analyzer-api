from pydantic import BaseModel


class SymbolRow(BaseModel):
    symbol: str
    last_refreshed: str
    last_checked: str
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
