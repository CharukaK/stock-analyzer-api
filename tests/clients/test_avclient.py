import httpx
import pytest
from pytest_httpx import HTTPXMock

from app.clients import AlphaVantageClient

MOCK_RESPONSE = {
    "Meta Data": {
        "1. Information": "Monthly Prices",
        "2. Symbol": "IBM",
        "3. Last Refreshed": "2026-05-09",
        "4. Time Zone": "US/Eastern",
    },
    "Monthly Time Series": {
        "2026-04-30": {
            "1. open": "150.00",
            "2. high": "160.00",
            "3. low": "140.00",
            "4. close": "155.00",
            "5. volume": "1000000",
        }
    },
}


@pytest.mark.asyncio
async def test_monthly_api_data_fetch(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json=MOCK_RESPONSE)
    client = AlphaVantageClient()
    result = await client.get_monthly_price_data("IBM")
    await client.aclose()

    assert result.metadata.symbol == "IBM"
    assert "2026-04-30" in result.monthly_time_series
    assert result.monthly_time_series["2026-04-30"].close == 155

@pytest.mark.asyncio
async def test_get_monthly_price_data_http_error(httpx_mock: HTTPXMock):
    httpx_mock.add_response(status_code=500)
    client = AlphaVantageClient()
    with pytest.raises(httpx.HTTPStatusError):
        await client.get_monthly_price_data("IBM")
    await client.aclose()


@pytest.mark.asyncio
async def test_get_monthly_price_data_invalid_json(httpx_mock: HTTPXMock):
    from pydantic import ValidationError
    httpx_mock.add_response(json={"unexpected": "data"})
    client = AlphaVantageClient()
    with pytest.raises(ValidationError):
        await client.get_monthly_price_data("IBM")
    await client.aclose()
