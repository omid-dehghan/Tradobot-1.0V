from IMarket.datafetcher import FetchData
from IExchange.exchangeprofile import ExProfile
from announcer import Announcer

class MarketSnapshot:
    """Calculations"""
#========================================== Class Attributes ========================================== 

    
#========================================== Constructor ========================================== 

    def __init__(self, announcer:Announcer, base=None, quote=None, constant=None) -> None:
        """gets 2 ticker data and check if trade profitable or not"""
        self.announcer = announcer
        self.setBase(base)
        self.setQuote(quote)
        self.setConstant(constant)
        self.setBaseObj(FetchData(announcer))
        self.setQuoteObj(FetchData(announcer))
        
                 
#========================================== Object Methods ==========================================      

    def fetch(self) -> None:
        self.getBaseObj().ticker = f"{self.getBase()}{self.getConstant()}"
        self.getQuoteObj().ticker = f"{self.getQuote()}{self.getConstant()}"
        self.getBaseObj().fetch()
        self.getQuoteObj().fetch()
        self.sets() 
        self.announcer.mms_position_announce(self.getBase(), self.getQuote(), self.MMb2q_sellprice, self.MMb2q_buyprice, self.MMb2q_profitloss, self.MMq2b_sellprice, self.MMq2b_buyprice, self.MMq2b_profitloss) 
    
    def sets(self) -> None:
        self.setExtractedDatas()
        self.__setMakerMakerStrategyPL()
        
#========================================== Setters ========================================== 

    def setExtractedDatas(self) -> dict:
        """Return The first order of 2 pairs: price and amount"""
        datas = {self.getBase(): {"asks":self.getBaseObj().get_orderbook("asks", 0),
                         "bids":self.getBaseObj().get_orderbook("bids", 0)},
                 self.getQuote(): {"asks":self.getQuoteObj().get_orderbook("asks", 0),
                         "bids":self.getQuoteObj().get_orderbook("bids", 0)}}
        self.__datas = datas

    def setBase(self, base) -> None:
        self.__base = base 
    def setQuote(self, quote) -> None:
        self.__quote = quote
    def setConstant(self, constant) -> None:
        self.__constant = constant
    def setBaseObj(self, fd) -> None:
        self.__BaseData = fd
    def setQuoteObj(self, fd) -> None:
        self.__QuoteData = fd
        
    def __setMakerMakerStrategyPL(self):
        # ------------- Maker Maker Base to Quote:
        self.__setMMb2q_sellprice(self.getExtractedDatas()[self.getBase()]["asks"]["price"])
        self.__setMMb2q_buyprice(self.getExtractedDatas()[self.getQuote()]["bids"]["price"])
        diff = self.getPriceGap(self.MMb2q_sellprice, self.MMb2q_buyprice)
        diff_percent = self.getPriceGapPercentage(diff, self.MMb2q_buyprice)
        self.__setMMb2q_profitloss(round(diff_percent - (2 * ExProfile.Maker_fee(self.getConstant())), 2))
        # ------------- Maker Maker Quote to Base:
        self.__setMMq2b_sellprice(self.getExtractedDatas()[self.getQuote()]["asks"]["price"])
        self.__setMMq2b_buyprice(self.getExtractedDatas()[self.getBase()]["bids"]["price"]) 
        diff = self.getPriceGap(self.MMq2b_sellprice, self.MMq2b_buyprice)
        diff_percent = self.getPriceGapPercentage(diff, self.MMq2b_sellprice)
        self.__setMMq2b_profitloss(round(diff_percent - (2 * ExProfile.Maker_fee(self.getConstant())), 2))

    def __setMMb2q_buyprice(self, price) -> float:
        self.__MMb2q_buyprice = price
    def __setMMb2q_sellprice(self, price) -> float:
        self.__MMb2q_sellprice = price
    def __setMMb2q_profitloss(self, pl) -> float:
        self.__MMb2q_profitloss = pl
    def __setMMq2b_buyprice(self, price) -> float:
        self.__MMq2b_buyprice = price
    def __setMMq2b_sellprice(self, price) -> float:
        self.__MMq2b_sellprice = price
    def __setMMq2b_profitloss(self, pl) -> float:
        self.__MMq2b_profitloss = pl

#========================================== Getters ========================================== 

    def getExtractedDatas(self) -> dict:
        return self.__datas   
    def getBase(self) -> str:
        return self.__base  
    def getQuote(self) -> str:
        return self.__quote 
    def getConstant(self) -> str:
        return self.__constant  
    def getBaseObj(self) -> FetchData:
        return self.__BaseData
    def getQuoteObj(self) -> FetchData:
        return self.__QuoteData    
    
    @property
    def MMb2q_buyprice(self) -> float:
        return self.__MMb2q_buyprice
    @property
    def MMb2q_sellprice(self) -> float:
        return self.__MMb2q_sellprice
    @property
    def MMb2q_profitloss(self) -> float:
        return self.__MMb2q_profitloss
    @property
    def MMq2b_buyprice(self) -> float:
        return self.__MMq2b_buyprice
    @property
    def MMq2b_sellprice(self) -> float:
        return self.__MMq2b_sellprice
    @property
    def MMq2b_profitloss(self) -> float:
        return self.__MMq2b_profitloss
    
    def getPriceGap(self, num1, num2):
        return num1 - num2
    def getPriceGapPercentage(self, num1, num2):
        return (num1 / num2) * 100