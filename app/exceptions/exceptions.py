class SymbolNotFoundError(Exception):
    def __init__(self, symbol: str, year: int) -> None:
        self._symbol: str = symbol
        self._year: int = year
        super().__init__(f"no data found for symbol {symbol} in {year}")

class ExternalAPIError(Exception):
    def __init__(self, message: str = "error reaching data provider") -> None:
        super().__init__(message)

class DataBaseError(Exception):
    def __init__(self, message: str = "database error occured") -> None:
        super().__init__(message)
