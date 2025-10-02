import requests
from IMarket.crypto_exchanges.base import IMarketDataFetcher
from announcer import Announcer

class Nobitex(IMarketDataFetcher):
    """Fetches market data from Nobitex API."""

    def __init__(self, announcer: Announcer) -> None:
        """Initialize the data fetcher."""
        self.announcer = announcer

    def fetch(self):
        self.fetch_raw_data()

    def fetch_raw_data(self) -> dict:
        """Fetch raw data from Nobitex API for the specified ticker."""
        try:       
            url = f"https://apiv2.nobitex.ir/v3/orderbook/{self.ticker}"
            response = requests.get(url, timeout=7)
            self.announcer.log(f"[Nobitex] {self.ticker} request...")
            if response.status_code == 200:
                self.announcer.log(f"[Nobitex] {self.ticker} ok...")
                self.data = response.json()
        except requests.exceptions.Timeout:
            self.announcer.error(f"{self.ticker} data request timeout...")
        except requests.exceptions.ConnectionError:
            self.announcer.error(f"{self.ticker} data request: Connection error. check your network...")
        except requests.exceptions.HTTPError as httperror:
            self.announcer.error(f"{self.ticker} data request: Http Error.{httperror}")
        except Exception as error:
            self.announcer.error(f"{error}")
        
    def get_orderbook(self, asksorbids, row) -> list:
        lst = [float(n) for n in self.data[asksorbids][row]]
        return {"price": lst[0],
                "amount": lst[1]}
        
    @property
    def ticker(self) -> str:
        """Get the ticker symbol."""
        if self.__ticker:
            return self.__ticker
        else:
            raise ValueError("Ticker must be set before fetching data.")

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
            self.announcer.error("Data has not been fetched yet.")

    @data.setter
    def data(self, data: dict) -> None:
        """Set the fetched data."""
        if isinstance(data, dict):
            self.__data = data
        else:
            self.announcer.error("data should be a dictionary.")
            