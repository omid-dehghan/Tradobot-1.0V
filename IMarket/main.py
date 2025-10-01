from datafetcher import FetchData
from dataloader import DataLoader
from crypto_exchanges.nobitex import Nobitex

if __name__ == "__main__":
    app = FetchData(Nobitex())
    app.fetch_data("XAUTUSDT")
    print(app.status)
    
    