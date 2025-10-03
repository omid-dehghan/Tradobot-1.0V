import requests
from IExchange.exchangeprofile import ExProfile
from IExchange.order import Order
import exceptions
import json

class TradeExecution(ExProfile):

    # ========================================== Attributes ==========================================



# ========================================== Constractors ==========================================

    def __init__(self) -> None:
        """This class will Execute Trades"""
        super().__init__()
        self.wallet = Wallet()

# ========================================== limit Order ==========================================

    def limit_order(self, order):
        """PRICE ---> Rial,\n
        AMOUNT ---> srcCurrency"""
        if not isinstance(order, Order):
            raise exceptions.TypeError(
                "arg should be instance of order class.")
        try:
            url = 'https://api.nobitex.ir/market/orders/add'
            params = {"type": order.orderType,
                      "srcCurrency": order.srcCurrency,
                      "dstCurrency": order.dstCurrency,
                      "amount": str(order.amount),
                      "price": order.price,
                      "clientOrderId": order.clientOrder
                      }
            response = requests.post(
                url=url, headers=self.Headers, data=json.dumps(params), timeout=10)
            if response.json()["status"] != "failed":
                print(
                    f"\n----------------------------\nOrder Placed Successfully: {response.json()}\n----------------------------\n")
                self.signal.emit(
                    f"\n----------------------------\nOrder Placed Successfully: {response.json()}\n----------------------------\n")
            else:
                self.signal.emit(
                    f"Error: {response.status_code} {response.text}")
            return response.json()
        except requests.exceptions.Timeout:
            self.signal.emit("limit order request timeout...")
        except requests.exceptions.ConnectionError:
            self.signal.emit(
                "limit order request: Connection error. check your network...")
        except requests.exceptions.HTTPError as httperror:
            self.signal.emit(f"limit order request: Http Error.{httperror}")
        except Exception as error:
            self.signal.emit(f"{error}")

# ========================================== Delete Order ==========================================

    def delete_order(self, clientOrderId):
        try:
            url = 'https://api.nobitex.ir/market/orders/update-status'
            params = {
                "clientOrderId": clientOrderId,
                "status": "canceled"
            }
            response = requests.post(
                url=url, headers=self.Headers, data=json.dumps(params), timeout=10)
            if response.status_code == 200:
                print(
                    f"Order Successfull Deleted: {response.json()}")
                self.signal.emit(
                    f"Order Successfull Deleted: {response.json()}")
            else:
                print(
                    f"failed: {response.json()}")
                self.signal.emit(
                    f"Error: {response.status_code} {response.text}")
        except requests.exceptions.Timeout:
            self.signal.emit("delete order request timeout...")
        except requests.exceptions.ConnectionError:
            self.signal.emit(
                "delete order request: Connection error. check your network...")
        except requests.exceptions.HTTPError as httperror:
            self.signal.emit(f"delete order request: Http Error.{httperror}")
        except Exception as error:
            self.signal.emit(f"{error}")

# ========================================== Order Status ==========================================

    def status_order(self, clientOrderId):
        try:
            url = 'https://api.nobitex.ir/market/orders/status'
            params = {
                "clientOrderId": clientOrderId,
            }
            response = requests.post(
                url=url, headers=self.Headers, data=json.dumps(params), timeout=10)
            if response.status_code == 200:
                print(f"Order: {response.json()}")
                self.signal.emit(f"Order: {response.json()}")
                return True
            else:
                self.signal.emit(
                    f"Error: {response.status_code} {response.text}")
        except requests.exceptions.Timeout:
            self.signal.emit("order status request timeout...")
        except requests.exceptions.ConnectionError:
            self.signal.emit(
                "order status request: Connection error. check your network...")
        except requests.exceptions.HTTPError as httperror:
            self.signal.emit(f"order status request: Http Error.{httperror}")
        except Exception as error:
            self.signal.emit(f"{error}")
