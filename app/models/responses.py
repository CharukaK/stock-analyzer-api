from pydantic import BaseModel


class AnnualSummaryResponse(BaseModel):
    high: str
    low: str
    volume: str
