from crypto_exchanges.bitpin import Bitpin
from crypto_exchanges.nobitex import Nobitex
from crypto_exchanges.base import IMarketDataFetcher

class FetchData:

    def __init__(self, ex:IMarketDataFetcher = Nobitex()):
        self.ex = ex

    def fetch_data(self, ticker):
        self.ex.fetch(ticker=ticker)
        
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



