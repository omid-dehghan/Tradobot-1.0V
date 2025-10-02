from IMarket.crypto_exchanges.bitpin import Bitpin
from IMarket.crypto_exchanges.nobitex import Nobitex
from IMarket.crypto_exchanges.base import IMarketDataFetcher

class FetchData:

    def __init__(self, announcer, ex:IMarketDataFetcher = None):
        if ex is None:
            ex = Nobitex(announcer) 
        self.ex = ex

    def fetch(self):
        self.ex.fetch()
        
    def get_orderbook(self, asksorbids, row):
        return self.ex.get_orderbook(asksorbids, row)

    @property
    def status(self):
        return self.data['status']

    @property
    def last_update(self):
        return self.data['lastUpdate']

    @property
    def last_trade_price(self):
        return self.data['lastTradePrice']

    @property
    def data(self) -> dict:
        """Get the fetched data."""
        try:
            return self.ex.data
        except AttributeError:
            raise AttributeError("Data has not been fetched yet.")

    @property
    def ticker(self) -> dict:
        """ticker setter"""
        try:
            return self.ex.ticker
        except AttributeError:
            raise AttributeError("set the ticker.")
        
    @ticker.setter
    def ticker(self, ticker) -> dict:
        """ticker setter"""
        self.ex.ticker = ticker
        
