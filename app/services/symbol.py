import aiosqlite
from app.clients import AlphaVantageClient
from app.db.repositories import SymbolsRepository, PricesRepository


class SymbolService:
    def __init__(
        self,
        av_client: AlphaVantageClient,
        symbol_repository: SymbolsRepository,
        prices_repository: PricesRepository,
    ) -> None:
        self._av_client: AlphaVantageClient = av_client
        self._symbol_repository: SymbolsRepository = symbol_repository
        self._prices_repository: PricesRepository = prices_repository

    def get_symbol_data_annual(self, symbol: str, year: int) -> None:

        print("recieved", symbol, year)
