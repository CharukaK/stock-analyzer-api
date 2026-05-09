from datetime import datetime
from typing import ClassVar
from pydantic import BaseModel, ConfigDict, Field


class MetaData(BaseModel):
    information: str = Field(alias="1. Information")
    symbol: str = Field(alias="2. Symbol")
    last_refreshed: datetime = Field(alias="3. Last Refreshed")
    time_zone: str = Field(alias="4. Time Zone")

    model_config: ClassVar[ConfigDict] = ConfigDict(populate_by_name=True)


class MonthlyDataPoint(BaseModel):
    open: float = Field(alias="1. open")
    high: float = Field(alias="2. high")
    low: float = Field(alias="3. low")
    close: float = Field(alias="4. close")
    volume: int = Field(alias="5. volume")

    model_config: ClassVar[ConfigDict] = ConfigDict(populate_by_name=True)


class AlphaVantageMonthlyResponse(BaseModel):
    metadata: MetaData = Field(alias="Meta Data")
    monthly_time_series: dict[str, MonthlyDataPoint] = Field(
        alias="Monthly Time Series"
    )

    model_config: ClassVar[ConfigDict] = ConfigDict(populate_by_name=True)
