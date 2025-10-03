import exceptions

class Order():
    """This class is just attributes and no behavior"""

    def __init__(self, orderType: str, srcCurrency: str, dstCurrency: str, amount: float, price: float, clientOrder: str = str(int(time.time() * 1000))):
        self.orderType = orderType
        self.srcCurrency = srcCurrency
        self.dstCurrency = dstCurrency
        self.price = price
        self.amount = amount
        self.clientOrder = clientOrder

    @property
    def orderType(self):
        return self.__orderType

    @property
    def srcCurrency(self):
        return self.__srcCurrency

    @property
    def dstCurrency(self):
        return self.__dstCurrency

    @property
    def amount(self):
        return self.__amount

    @property
    def price(self):
        return self.__price

    @property
    def clientOrder(self):
        return self.__clientOrder

    @orderType.setter
    def orderType(self, orderType: str):
        if not isinstance(orderType, str):
            raise exceptions.TypeError("order type", "string")
        if orderType.lower() != "buy" and orderType.lower() != "sell":
            raise exceptions.OrderTypeError
        self.__orderType = orderType.lower()

    @srcCurrency.setter
    def srcCurrency(self, srcCurrency):
        if not isinstance(srcCurrency, str):
            raise exceptions.TypeError("src currency", "string")
        if srcCurrency.lower() != "xaut" and srcCurrency.lower() != "paxg" and srcCurrency.lower() != "usdt" and srcCurrency.lower() != "dai":
            raise exceptions.SrcCurrencyError
        self.__srcCurrency = srcCurrency.lower()

    @dstCurrency.setter
    def dstCurrency(self, dstCurrency):
        if not isinstance(dstCurrency, str):
            raise exceptions.TypeError("dst currency", "string")
        if dstCurrency.lower() != "usdt" and dstCurrency.lower() != "rls":
            raise exceptions.DstCurrencyError
        self.__dstCurrency = dstCurrency

    @amount.setter
    def amount(self, amount):
        atleast = 5
        if not isinstance(amount, float) and not isinstance(amount, int):
            raise exceptions.TypeError("amount", "float")
        if self.srcCurrency == "paxg" or self.srcCurrency == "xaut":
            if self.price * amount < atleast:
                raise exceptions.AmountError(
                    f"amount should be greater equal than {atleast / self.price}")
        elif self.srcCurrency == "dai" or self.srcCurrency == "usdt":
            if amount < atleast:
                raise exceptions.AmountError(
                    f"amount should be greater equal than {atleast}!")
        self.__amount = amount

    @price.setter
    def price(self, price):
        if not isinstance(price, float) and not isinstance(price, int):
            raise exceptions.TypeError("price", "float")
        if price < 0.00001:
            raise exceptions.PriceError
        self.__price = price

    @clientOrder.setter
    def clientOrder(self, clientOrder):
        if not isinstance(clientOrder, str):
            raise exceptions.TypeError("client order", "string")
        self.__clientOrder = clientOrder

