import requests
from crypto_exchanges.base import IMarketDataFetcher


class Bitpin(IMarketDataFetcher):
    """Fetches market data from Bitpin API."""

    def __init__(self) -> None:
        """Initialize the data fetcher."""
        pass

    def fetch_raw_data(self, ticker) -> dict:
        """Fetch raw data from Bitpin API for the specified ticker."""
        self.ticker = ticker
        url = f"https://api.bitpin.org/api/v1/mth/orderbook/{self.ticker}/"
        response = requests.get(url, timeout=10)
        self.data = response.json()
        return self.data

    def get_symbols(self) -> dict:
        """Fetch raw data from Bitpin API for the specified ticker."""
        url = f"https://api.bitpin.org/api/v1/mkt/markets/"
        response = requests.get(url, timeout=10)
        return response.json()

    @property
    def ticker(self) -> str:
        """Get the ticker symbol."""
        try:
            return self.__ticker
        except AttributeError:
            ("Ticker must be set before fetching data.")

    @ticker.setter
    def ticker(self, ticker: str) -> None:
        """
        Tickers:\nBTCUSDT,\nETHUSDT,\nUSDTIRT,\nDAIIRT,\nPAXGUSDT,\nXAUTUSDT
        """
        if ticker.lower() not in [
            "btc_usdt", "eth_usdt", "usdt_irt", "dai_irt", "paxg_usdt", "xaut_usdt"
        ]:
            raise ValueError(
                "Invalid ticker. Please use a valid ticker symbol.")
        self.__ticker = ticker.upper()

    @property
    def data(self) -> dict:
        """Get the fetched data."""
        try:
            return self.__data
        except AttributeError:
            raise AttributeError("Data has not been fetched yet.")

    @data.setter
    def data(self, data: dict) -> None:
        """Set the fetched data."""
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary.")
        self.__data = data
