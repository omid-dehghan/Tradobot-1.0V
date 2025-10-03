import exceptions

class Receipt():
    """Order Placed Successfully: {'status': 'ok', 'order': 
    {'type': 'sell', 'execution': 'Limit', 'tradeType': 'Spot', 'srcCurrency': 'TetherGold',
      'dstCurrency': 'Tether', 'price': '2931.4', 'amount': '0.004', 'totalPrice': '0',
        'totalOrderPrice': '11.7256', 'matchedAmount': '0', 'unmatchedAmount': '0.004',
          'clientOrderId': '55555', 'isMyOrder': False, 'id': 2724716125, 'status': 'Active',
            'partial': False, 'fee': '0', 'user': 'dehghanfinancial@gmail.com',
              'created_at': '2025-03-05T09:35:25.733430+00:00', 'market': 'XAUT-USDT',
                'averagePrice': '0'}}"""

    def __init__(self, receipt: dict, isOptimal:bool=True):
        if receipt == None:
            raise exceptions.ReceiptNoneTypeError
        else:
            if receipt["status"] == "failed":
                raise exceptions.ReceiptStatusError(receipt["code"])
            self.receipt = receipt
            self.orderType = receipt["order"]["type"]
            self.srcCurrency = self.srcAndDst(
                receipt["order"]["market"])["src"]
            self.dstCurrency = self.srcAndDst(
                receipt["order"]["market"])["dst"]
            self.price = float(receipt["order"]["price"])
            self.amount = float(receipt["order"]["amount"])
            self.amount_usdt = float(receipt["order"]["totalOrderPrice"])
            self.clientOrderId = receipt["order"]["clientOrderId"]
            self.isOptimal = isOptimal

    def srcAndDst(self, pair: str):
        src = pair[:4].lower()
        dst = pair[-4:].lower()
        return {"src": src, "dst": dst}

