from fastapi import Request
from app.clients import AlphaVantageClient


def get_alphavantage_client(request: Request) -> AlphaVantageClient:
    return request.app.state.alphavantage_client
