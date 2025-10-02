class ExProfile:
    __token = "499ee0727191e2e25253ab66bc8b79c32cd02419"
    __headers = {"Authorization": f"Token {__token}",
                 "Content-Type": "application/json"}

    @property
    def Headers(self):
        return self.__headers

    @property
    def Token(self):
        return self.__token
    
    def Taker_fee(constant) -> float:
        if constant == "USDT":
            return 0.12
        if constant == "IRT":
            return 0.20
    
    def Maker_fee(constant) -> float:
        if constant == "USDT":
            return 0.095
        if constant == "IRT":
            return 0.17
