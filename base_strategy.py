import pandas as pd
from utils import orderDirection
from Quote import Quote
from Account import Account



def genSignal(Series):
    if Series["close"] + 10 > Series["20ma"]:
        return orderDirection.SHORT_OPEN
    elif Series["close"] - 10 < Series["20ma"]:
        return orderDirection.LONG_OPEN
    

    return -1



def myStrategy(account: Account, data: pd.DataFrame, quote:Quote):
    """策略
    data: K线
    dataFrame 必须有的三个列属性：
    tradingFlag: orderDirection.SHORT_OPEN or others
    tradingVol: int
    tradingPrice: float
    """
    data["20ma"] = data["close"].rolling(window=20).mean()
    
    data["tradingFlag"] = data.apply(genSignal) # 该策略是当收盘价大于20日均线+10的时候开空单，小于20日均线-10的时候开多单
    # data["tradingVol"] = 
    # data[""]
    # 平仓策略必须写在分钟K线的外面，否则行情突变可能强平或爆仓

    
    pass