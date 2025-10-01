from abc import ABC, abstractmethod


class IMarketDataFetcher(ABC):


    @abstractmethod
    def fetch(self, ticker):
        pass

    @abstractmethod
    def fetch_raw_data(self, ticker):
        pass
    
    @abstractmethod
    def get_orderbook(self, asksorbids, row):
        pass 

    # @property
    # @abstractmethod
    # def status(self):
    #     self.data['status']

    # @property
    # @abstractmethod
    # def last_update(self):
    #     self.data['lastUpdate']

    # @property
    # @abstractmethod
    # def last_trade_price(self):
    #     self.data['lastTradePrice']

    @property
    @abstractmethod
    def ticker(self) -> str:
        """Get the ticker symbol."""
        pass

    @ticker.setter
    @abstractmethod
    def ticker(self, ticker: str) -> None:
        """
        Tickers:\nBTCUSDT,\nETHUSDT,\nUSDTIRT,\nDAIIRT,\nPAXGUSDT,\nXAUTUSDT
        """
        pass

    @property
    @abstractmethod
    def data(self) -> dict:
        """Get the fetched data."""
        pass

    @data.setter
    @abstractmethod
    def data(self, data: dict) -> None:
        """Set the fetched data."""
        pass
