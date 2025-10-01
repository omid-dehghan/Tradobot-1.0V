import requests
from crypto_exchanges.base import IMarketDataFetcher

class Nobitex(IMarketDataFetcher):
    """Fetches market data from Nobitex API."""

    def __init__(self) -> None:
        """Initialize the data fetcher."""
        pass

    def fetch(self, ticker):
        self.fetch_raw_data(ticker)

    def fetch_raw_data(self, ticker) -> dict:
        """Fetch raw data from Nobitex API for the specified ticker."""
        try:
            self.ticker = ticker        
            url = f"https://apiv2.nobitex.ir/v3/orderbook/{self.ticker}"
            response = requests.get(url, timeout=10)
            self.data = response.json()
        except requests.exceptions.Timeout:
            print(f"{self.ticker} data request timeout...")
        except requests.exceptions.ConnectionError:
            print(f"{self.ticker} data request: Connection error. check your network...")
        except requests.exceptions.HTTPError as httperror:
            print(f"{self.ticker} data request: Http Error.{httperror}")
        except Exception as error:
            print(f"{error}")
        
    def get_orderbook(self, asksorbids, row):
        return self.data[asksorbids][row]
    
    @property
    def status(self):
        self.data['status']

    @property
    def last_update(self):
        self.data['lastUpdate']

    @property
    def last_trade_price(self):
        self.data['lastTradePrice']
        
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
            "btcusdt", "ethusdt", "usdtirt", "daiirt", "paxgusdt", "xautusdt"
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