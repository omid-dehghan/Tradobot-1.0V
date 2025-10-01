from IMarket.datafetcher import FetchData
from IMarket.dataloader import DataLoader
from IMarket.crypto_exchanges.nobitex import Nobitex
from marketsnapshot import MarketSnapshot

if __name__ == "__main__":
    app = MarketSnapshot("XAUT", "PAXG", "USDT")
    app.fetch()
    
    print(app.MMb2q_profitloss)
    print(app.MMq2b_profitloss)
    
