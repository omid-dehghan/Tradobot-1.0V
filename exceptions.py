# ======================================== Auto Trade Exceptions ===========================================
class AutoTradeException(Exception):
    """Base Class for all exceptions related to automatic trade process"""
    pass


class NoProfitIdentified(AutoTradeException):
    """Raised when conversion has no profit"""

    def __init__(self, pl1="N/A", pl2="N/A", message="No profit in conversion"):
        self.pl1 = pl1
        self.pl2 = pl2
        super().__init__(f"{message}: {pl1}%, {pl2}%")

# ======================================== Order Exceptions ===========================================


class OrderValidationException(Exception):
    """Base Class for all exception related to Ordering"""
    pass


class TypeError(OrderValidationException):
    """Raised when type of order is not valid"""

    def __init__(self, arg="argument", expected_type="valid"):
        message = f"type of {arg} should be {str(expected_type)}!"
        super().__init__(message)


class OrderTypeError(OrderValidationException):
    """Raised when type of order is not valid"""

    def __init__(self, message="type should be string, 'buy' or 'sell'!"):
        super().__init__(message)


class SrcCurrencyError(OrderValidationException):
    """Raised when srcCurrency of order is not valid"""

    def __init__(self, message="srcCurrency should be string, 'xaut', 'paxg', 'dai', 'usdt'..."):
        super().__init__(message)


class DstCurrencyError(OrderValidationException):
    """Raised when dstCurrency of order is not valid"""

    def __init__(self, message="dstCurrency should be string, 'usdt' or 'rls'!"):
        super().__init__(message)


class AmountError(OrderValidationException):
    """Raised when amount of order is not valid"""

    def __init__(self, message="amount is not valid!"):
        super().__init__(message)


class PriceError(OrderValidationException):
    """Raised when price of order is not valid"""

    def __init__(self, message="price should be float, you have to enter valid price!"):
        super().__init__(message)


class ClientOrderException(OrderValidationException):
    """Raised when ClientOrder of order is not valid"""
    pass


class DuplicatedClientOrderError(ClientOrderException):
    """Raised when ClientOrder already used"""

    def __init__(self, message="ClientOrder should be unique!"):
        super().__init__(message)


class ClientOrderTypeError(ClientOrderException):
    """Raised when ClientOrder type is not valid"""

    def __init__(self, message="ClientOrder should be string!"):
        super().__init__(message)

class ReceiptException(Exception):
    """Receipt problem"""
    pass
class ReceiptStatusError(ReceiptException):
    """Raised when order was not successful!"""
    def __init__(self, code, message="Order failed"):
        description = "order not valid."
        if code == "InvalidOrderPrice":
            description = "order price isn't determined or is wrong!"
        if code == "BadPrice":
            description = """In a normal order: The price set for the order is very different from the current market price. Set your order price within 30% of the current market price.
In a stop-loss order: The price set for the market order cannot be better than the stop price."""
        if code == "PriceConditionFailed":
            description = "The price condition is not included in the order. The price condition is defined between the price parameters and the market price."
        if code == "OverValueOrder":
            description = "balance is not enough."
        if code == "SmallOrder":
            description = "The minimum transaction value has not been met. The minimum transaction value for Rial markets is 3 million Rials and for tether markets, it is 5 tether, and the total order amount (amount*price) must be greater than this minimum."
        if code == "DuplicateOrder":
            description = "An order with the same specifications was submitted by your user in the last 10 seconds."
        if code == "InvalidMarketPair":
            description = "The source currency (srcCurrency) or destination currency (dstCurrency) is not set correctly or such a market does not exist on Nobitex."
        if code == "MarketClosed":
            description = "The market in question is currently temporarily closed."
        if code == "TradingUnavailable":
            description = "The user is not authorized to trade, complete your authentication process."
        if code == "FeatureUnavailable":
            description = "You are not a user authorized to use trial features."
        if code == "DuplicateClientOrderId":
            description = "The user order ID is duplicated (only one open/active/inactive order with one order number is possible for each user at a time)."
        if code == "ParseError":
            description = "The input format does not match the required format."
        super().__init__(f"{message} - {code}: {description}")

class ReceiptNoneTypeError(ReceiptException):
    """Raised when Receipt is none type!"""
    def __init__(self, message="Receipt can not be 'NoneType'"):
        super().__init__(message)
if __name__ == "__main__":
    pass
