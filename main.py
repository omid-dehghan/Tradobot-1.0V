from IMarket.datafetcher import FetchData
from IMarket.dataloader import DataLoader
from IMarket.crypto_exchanges.nobitex import Nobitex
from marketsnapshot import MarketSnapshot
from announcer import Announcer
import time

if __name__ == "__main__":
    announcer = Announcer(printing=True, save_to_file=False)
    app = MarketSnapshot(announcer, "PAXG", "XAUT", "USDT")
    while True:
        try:
            app.fetch()
            announcer.info(announcer.logs)
            time.sleep(8)
        except Exception as error:
            announcer.error(error)