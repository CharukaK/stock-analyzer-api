import httpx
from app.core import settings
from app.models import AlphaVantageMonthlyResponse

TIMEOUT = 10


class AlphaVantageClient:
    def __init__(self) -> None:
        self.api_key: str = settings.ALPHAVANTAGE_API_KEY
        self._client: httpx.AsyncClient = httpx.AsyncClient(
            timeout=TIMEOUT, base_url=settings.ALPHAVANTAGE_URL
        )

    async def get_monthly_price_data(self, symbol: str) -> AlphaVantageMonthlyResponse:
        # https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=IBM&apikey=demo
        params = {
            "function": "TIME_SERIES_MONTHLY",
            "symbol": symbol,
            "apikey": self.api_key,
        }

        response = await self._client.get("query", params=params)
        _ = response.raise_for_status()
        return AlphaVantageMonthlyResponse.model_validate(response.json())

    async def aclose(self) -> None:
        await self._client.aclose()
