import pandas as pd
from utils import orderDirection
from Quote import Quote
from Account import Account



def genOpenSignal(Series):
    # print(Series)
    if Series.close - 10 > Series.ma20:
        return orderDirection.SHORT_OPEN
    elif Series.close + 10 < Series.ma20:
        return orderDirection.LONG_OPEN
    return -1


def genStopEarnSignal(Series):
    if Series.tradingFlag == orderDirection.LONG_OPEN:
        return Series.tradingPrice + 8
    elif Series.tradingFlag == orderDirection.SHORT_OPEN:
        return Series.tradingPrice - 8
    return -1


def genStopLossSignal(Series):
    if Series.tradingFlag == orderDirection.LONG_OPEN:
        return Series.tradingPrice - 8
    elif Series.tradingFlag == orderDirection.SHORT_OPEN:
        return Series.tradingPrice + 8
    return -1


def myStrategy(data: pd.DataFrame):
    """策略
    data: K线
    dataFrame 必须有的三个列属性：
    tradingFlag: orderDirection.SHORT_OPEN or others
    tradingVol: int
    tradingPrice: float 开仓价格 or 主动平仓价格
    stopEarnPrice: float 止盈价
    stopLossPrice: float 止损价
    """
    data["ma20"] = data["close"].rolling(window=20).mean()
    

    # 也就是说开仓的时候已经把止盈止损线弄好了，但是策略行情里面怎么监视这个止盈止损线呢？
    data["tradingFlag"] = data.apply(genOpenSignal, axis=1) # 该策略是当收盘价大于20日均线+10的时候开空单，小于20日均线-10的时候开多单
    data["tradingVol"] = 1
    data["tradingPrice"] = data["close"]
    data["stopEarnPrice"] = data.apply(genStopEarnSignal, axis=1)
    data["stopLossPrice"] = data.apply(genStopLossSignal, axis=1)
    
    # K线的平仓策略也是允许的
    
    # 止盈 平仓策略必须写在分钟K线的外面，否则行情突变可能强平或爆仓
    return data