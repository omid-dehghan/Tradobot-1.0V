from IExchange.exchangeprofile import ExProfile
import requests
import json
from announcer import Announcer

class Wallet(ExProfile):


    def __init__(self, announcer:Announcer):
        super().__init__()
        self.announcer = announcer


    def balance(self, currency: str):
        """60 requests in 2 minutes"""
        try:
            url = 'https://api.nobitex.ir/users/wallets/balance'
            h = {"Authorization": f"Token {self.Token}"}
            params = {
                "currency": currency,
            }
            response = requests.post(
                url=url, headers=h, data=json.dumps(params), timeout=10)
            if response.status_code == 200:
                return float(response.json()["balance"])
            else:
                self.announcer.error(f"Error: {response.status_code} {response.text}")
        except requests.exceptions.Timeout:
            self.announcer.error("balance request timeout...")
        except requests.exceptions.ConnectionError:
            self.announcer.error(
                "balance request: Connection error. check your network...")
        except requests.exceptions.HTTPError as httperror:
            self.announcer.error(f"balance request: Http Error.{httperror}")
        except Exception as error:
            self.announcer.error(f"{error}")
