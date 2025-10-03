from exceptions import NoProfitIdentified
from IExchange.tradeexecution import TradeExecution
from IExchange.order import Order
from IExchange.receipt import Receipt
from IExchange.autotrade import AutoTrade
from marketsnapshot import MarketSnapshot

import time


class AutoTrade:
    def __init__(self, snap=MarketSnapshot):
        self.snap = snap
        self.te = TradeExecution()
        self.optimalprice = 0

    @property
    def isProfitable(self) -> bool:
        return self.snap.MMb2q_profitloss > 0 or self.snap.MMq2b_buyprice > 0

    def ConversionDirection(self) -> dict:
        if self.isProfitable:
            if self.snap.MMb2q_profitloss > self.snap.MMq2b_profitloss:
                source = self.snap.getBaseDo()
                target = self.snap.getQuoteDo()
            else:
                source = self.snap.getQuoteDo()
                target = self.snap.getBaseDo()
            return {"start": source, "end": target}
        else:
            raise NoProfitIdentified(
                self.snap.MMb2q_profitloss, self.snap.MMq2b_profitloss)

    def getOptimalOrderPlace(self, do, asksorbids: str, max_depth, max_amount, my_order_amount = 0, my_order_price = 0) -> dict:
        """keys:\n
        "depth", "price", "orderprice"\n"""
        Queue_amount = 0
        depth = 0
        data = None
        while depth < max_depth:
            data = do.fromOrderBook(row=depth, asksorbids=asksorbids)
            depth += 1
            if data["price"] == my_order_price:
                if data["amount"] == my_order_amount:
                    max_depth += 1
                    continue
                else:
                    data["amount"] = data["amount"] - my_order_amount
            Queue_amount += data["amount"]
            if Queue_amount > (max_amount / do.getLastPrice()):
                break

        if do.getTicker()[:4] == "PAXG":
            if asksorbids == "asks" or asksorbids == "sell":
                order_price = data["price"] - 1
            else:
                order_price = data["price"] + 1
        elif do.getTicker()[:4] == "XAUT":
            if asksorbids == "asks" or asksorbids == "sell":
                order_price = data["price"] - 0.1
            else:
                order_price = data["price"] + 0.1

        elif do.getTicker()[:4] == "USDT" or do.getTicker()[:4] == "DAII":
            if asksorbids == "asks" or asksorbids == "sell":
                order_price = data["price"] - 10
            else:
                order_price = data["price"] + 10

        return {"depth": depth,
                "queueamount": Queue_amount,
                "queueamount_usdt": round(Queue_amount * data["price"], 5),
                "price": data["price"],
                "orderprice": round(order_price, 1)}

    def reOrder(self, order: Receipt, new_price: float) -> Receipt:
        self.te.delete_order(order.clientOrderId)
        def newAmount():
            return order.amount_usdt / new_price
        time.sleep(10)
        order = Receipt(self.te.limit_order(Order(order.orderType, order.srcCurrency,
                        order.dstCurrency, newAmount(), new_price, order.clientOrderId)))
        return order

    def OptimaizeOrderPlacement(self, do, receipt: Receipt, max_depth = 10, max_amount = 10000000000):
        if not self.isOptimal(do, receipt, max_depth = max_depth, max_amount = max_amount):
            receipt = self.reOrder(receipt, self.optimalprice)
        return receipt
    
    def isOptimal(self, at:AutoTrade, do, receipt: Receipt, max_depth, max_amount):
        data = at.getOptimalOrderPlace(
            do, receipt.orderType, max_depth = max_depth, max_amount = max_amount, my_order_amount = receipt.amount, my_order_price = receipt.price)
        self.optimalprice = data["orderprice"]
        print(self.optimalprice == receipt.price)
        print(self.optimalprice, receipt.price)
        if self.optimalprice == receipt.price:
            receipt.isOptimal = True
            return True
        else:
            receipt.isOptimal = False
            return False

    def getBaseProfitFrontier(self) -> float:
        return self.__base_profit_frontier

    def getQuoteProfitFrontier(self) -> float:
        return self.__quote_profit_frontier

    def setBaseProfitFrontier(self, number) -> None:
        self.__base_profit_frontier = number

    def setQuoteProfitFrontier(self, number) -> None:
        self.__quote_profit_frontier = number


if __name__ == "__main__":
    # from position import Position
    # p = Position("PAXG", "XAUT", "USDT")
    # at = AutoTrade(p)
    
    # myorder = Receipt(at.te.limit_order(Order("sell", "xaut", "usdt", 0.13, 3500)), False)
    # r = myorder
    # while True:
    #     try:
    #         if r.isOptimal == True:
    #             time.sleep(10)
    #         p.refreshData()
    #         r = at.OptimaizeOrderPlacement(p.getQuoteDo(), r,max_amount=100)
    #     except Exception as e:
    #         print(e)
    pass