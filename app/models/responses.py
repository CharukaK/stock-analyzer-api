from pydantic import BaseModel


class AnnualSummaryResponse(BaseModel):
    high: float
    low: float
    volume: int
