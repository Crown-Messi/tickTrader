import pandas as pd
import glob
from datetime import datetime, timedelta, time

pd.set_option('display.max_rows', 200)

def cleanMinData(filePath):
    """filePath: 1min k-line csv file"""
    data = pd.read_csv(filePath, encoding="gb18030")
    data.columns = ["market", "code", "date", "open", "high", "low", "close", "vol", "turnover", "tolposition"]
    # data.set_index("date", inplace=True, drop=False)
    return data

def concat1minData(csvDir):
    """1min data csvDir"""
    csvList = glob.glob(csvDir)
    csvList.sort()
    res = None
    for file in csvList:
        tmp = cleanMinData(file)
        res = tmp if res is None else pd.concat([res, tmp])
    return res

def cleanTickData(filePath):
    """filePath: tick csv file"""
    data = pd.read_csv(filePath, encoding="gb18030", dtype={"交易日":str, "最后修改毫秒":str})
    #  市场代码    合约代码    时间    最新    持仓   增仓   成交额    成交量    开仓    平仓    成交类型    方向    买一价    卖一价    买一量    卖一量
    """
    ["交易日","合约代码","交易所代码","合约在交易所的代码","最新价","上次结算价","昨收盘","昨持仓量","今开盘", \
        "最高价","最低价","数量","成交金额","持仓量","今收盘","本次结算价","涨停板价","跌停板价","昨虚实度","今虚实度", \
            "最后修改时间","最后修改毫秒","申买价一","申买量一","申买价二","申买量二","申买价三","申买量三","申买价四","申买量四","申买价五","申买量五", \
                "申卖价一","申卖量一","申卖价二","申卖量二","申卖价三","申卖量三","申卖价四","申卖量四","申卖价五","申卖量五","当日均价","业务日期"]
    """
    data["tick时间"] = data["交易日"]+ "." +data["最后修改时间"]+ "." + data["最后修改毫秒"]
    data["tick成交量"] = data["数量"].diff()
    data["tick成交额"] = data["成交金额"].diff()
    data.fillna(0)
    # data.columns = ["market", "code", "date", "new", "pos", "addpos", "turnover", "turnvol", "openVol", "closeVol","turntype", "direct", "bidprice1", "askprice1","bidvol1", "askvol1"]
    data.set_index("tick时间", inplace=True, drop=False)
    # print(data.head(20))
    return data

def tickQuote(csvDir):
    csvList = glob.glob(csvDir+"/*.csv")
    csvList = ["/home/ztcapital/Codes/FutureQuant/backTestData/tickMore/sp2405_20240201.csv"]
    csvList.sort()
    for csvfile in csvList:
        reader = cleanTickData(csvfile)
        # 遍历CSV文件中的每一行
        for index, row in reader.iterrows():
            # 生成并返回当前行数据
            Quote.TickTime           = index
            Quote.TradeDate          = row["交易日"]
            Quote.Instrument         = row["合约代码"]
            Quote.ExCode             = row["交易所代码"]
            Quote.InstrumentCodeInEx = row["合约在交易所的代码"]
            Quote.NewPrice           = row["最新价"]
            Quote.SettlementPrice    = row["上次结算价"]
            Quote.CloseYst           = row["昨收盘"]
            Quote.PositionYst        = row["昨持仓量"]
            Quote.OpenTd             = row["今开盘"]
            Quote.HighPrice          = row["最高价"]
            Quote.LowPrice           = row["最低价"]
            Quote.Volume             = row["数量"]
            Quote.Amount             = row["成交金额"]
            Quote.Position           = row["持仓量"]
            Quote.CloseTd            = row["今收盘"]
            Quote.Settlement         = row["本次结算价"]
            Quote.UpperLimit         = row["涨停板价"]
            Quote.LowerLimit         = row["跌停板价"]
            Quote.DeltaYst           = row["昨虚实度"]
            Quote.DeltaTd            = row["今虚实度"]
            Quote.LastMdfTime        = row["最后修改时间"]
            Quote.LastMdfMillSecond  = row["最后修改毫秒"]
            Quote.BuyPrice1          = row["申买价一"]
            Quote.BuyVolume1         = row["申买量一"]
            Quote.BuyPrice2          = row["申买价二"]
            Quote.BuyVolume2         = row["申买量二"]
            Quote.BuyPrice3          = row["申买价三"]
            Quote.BuyVolume3         = row["申买量三"]
            Quote.BuyPrice4          = row["申买价四"]
            Quote.BuyVolume4         = row["申买量四"]
            Quote.BuyPrice5          = row["申买价五"]
            Quote.BuyVolume5         = row["申买量五"]
            Quote.AskPrice1          = row["申卖价一"]
            Quote.AskVolume1         = row["申卖量一"]
            Quote.AskPrice2          = row["申卖价一"]
            Quote.AskVolume2         = row["申卖量一"]
            Quote.AskPrice3          = row["申卖价三"]
            Quote.AskVolume3         = row["申卖量三"]
            Quote.AskPrice4          = row["申卖价四"]
            Quote.AskVolume4         = row["申卖量四"]
            Quote.AskPrice5          = row["申卖价五"]
            Quote.AskVolume5         = row["申卖量五"]
            Quote.AvgTd              = row["当日均价"]
            Quote.ItemDate           = row["业务日期"]
            Quote.TickVolume         = row["tick成交量"]
            Quote.TickAmount         = row["tick成交额"]

            yield Quote

class Quote(object):
    """
    ["交易日","合约代码","交易所代码","合约在交易所的代码","最新价","上次结算价","昨收盘","昨持仓量","今开盘", \
        "最高价","最低价","数量","成交金额","持仓量","今收盘","本次结算价","涨停板价","跌停板价","昨虚实度","今虚实度", \
            "最后修改时间","最后修改毫秒","申买价一","申买量一","申买价二","申买量二","申买价三","申买量三","申买价四","申买量四","申买价五","申买量五", \
                "申卖价一","申卖量一","申卖价二","申卖量二","申卖价三","申卖量三","申卖价四","申卖量四","申卖价五","申卖量五","当日均价","业务日期"]
    """
    TradeDate           = None  # 交易日
    Instrument          = None  # 合约代码
    ExCode              = None  # 交易所代码
    InstrumentCodeInEx  = None  # 合约在交易所的代码
    NewPrice            = None  # 最新价
    SettlementPrice     = None  # 上次结算价
    CloseYst            = None  # 昨收盘
    PositionYst         = None  # 昨持仓量
    OpenTd              = None  # 今开盘
    HighPrice           = None  # 最高价
    LowPrice            = None  # 最低价
    Volume              = None  # 数量
    Amount              = None  # 成交金额
    Position            = None  # 持仓量
    CloseTd             = None  # 今收盘
    Settlement          = None  # 本次结算价
    UpperLimit          = None  # 涨停板价
    LowerLimit          = None  # 跌停板价
    DeltaYst            = None  # 昨虚实度
    DeltaTd             = None  # 今虚实度
    LastMdfTime         = None  # 最后修改时间
    LastMdfMillSecond   = None  # 最后修改毫秒
    BuyPrice1           = None  # 申买价一
    BuyVolume1          = None  # 申买量一
    BuyPrice2           = None  # 申买价二
    BuyVolume2          = None  # 申买量二
    BuyPrice3           = None  # 申买价三
    BuyVolume3          = None  # 申买量三
    BuyPrice4           = None  # 申买价四
    BuyVolume4          = None  # 申买量四
    BuyPrice5           = None  # 申买价五
    BuyVolume5          = None  # 申买量五
    AskPrice1           = None  # 申卖价一
    AskVolume1          = None  # 申卖量一
    AskPrice2           = None  # 申卖价一
    AskVolume2          = None  # 申卖量一
    AskPrice3           = None  # 申卖价三
    AskVolume3          = None  # 申卖量三
    AskPrice4           = None  # 申卖价四
    AskVolume4          = None  # 申卖量四
    AskPrice5           = None  # 申卖价五
    AskVolume5          = None  # 申卖量五
    AvgTd               = None  # 当日均价
    ItemDate            = None  # 业务日期
    TickTime            = None  # tick时间
    TickVolume          = None
    TickAmount          = None


#  用于合成K线 支持分钟级别
class KLine(object):

    def __init__(self, minutes=1, datalength=100) -> None:
        self.curMinute = None # 时间
        self.open = 0  # 开盘价
        self.close = 0 # 收盘价
        self.high = 0  # 最高价 
        self.low = 9999999999 # 最低价
        self.volume = 0 # 成交量
        self.amount = 0 # 成交额
        self.upperLimit = 0 # 涨停价
        self.lowerLimit = 0 # 跌停价
        self.minutes = minutes  # k线级别

        self.counter = 0
        self.datalength = datalength
        self.data = pd.DataFrame(columns=["time", "open", "high", "low", "close", "volume", "amount", "upperLimit", "lowerLimit"])

    def update(self, quote: Quote,):
        tickTime = datetime.strptime(quote.TickTime, "%Y%m%d.%H:%M:%S.%f")
        
        if  time(0, 0, 0) <  tickTime.time() < time(9, 0, 0) or time(15, 0, 0) <  tickTime.time() < time(21, 0, 0) or \
            time(10, 15, 0) <  tickTime.time() < time(10, 30, 0) or time(11, 30, 0) <  tickTime.time() < time(13, 30, 0) or\
            time(23, 0, 0) <  tickTime.time() < time(23, 59, 59):
            return  

        if self.curMinute is None:
            self.curMinute = datetime(tickTime.year, tickTime.month, tickTime.day, tickTime.hour, tickTime.minute, 0)
            self.open = quote.NewPrice

            if time(10,15,0) <= self.curMinute.time() < time(10,30,0) or time(15,0,0) <= self.curMinute.time() < time(21,0,0) or\
                time(0,0,0) <= self.curMinute.time() < time(9,0,0) or time(11,30,0) <= self.curMinute.time() < time(13,30,0) or \
                    time(23,0,0) <= self.curMinute.time() < time(23,59,59): 
                self.curMinute = None

        else:
            if not (self.curMinute  <=  tickTime < self.curMinute + timedelta(minutes=self.minutes)):
                
                if time(10,15,0) <= self.curMinute.time() < time(10,30,0) or time(15,0,0) <= self.curMinute.time() < time(21,0,0) or\
                    time(0,0,0) <= self.curMinute.time() < time(9,0,0) or time(11,30,0) <= self.curMinute.time() < time(13,30,0) or \
                        time(23,0,0) <= self.curMinute.time() < time(23,59,59): 
                    self.curMinute = None
                    return
                
                if self.counter < 50:
                    self.data.loc[self.counter] = [self.curMinute.strftime("%Y%m%d %H:%M:%S"), self.open, self.high, self.low, self.close, self.volume, self.amount, self.upperLimit, self.lowerLimit]
                else:
                    self.data.drop(0)
                    self.data.loc[len(self.data)] = [self.curMinute.strftime("%Y%m%d %H:%M:%S"), self.open, self.high, self.low, self.close, self.volume, self.amount, self.upperLimit, self.lowerLimit]
                    # print(self.counter, self.counter%self.datalength, self.data.loc[self.counter%self.datalength], sep="   ")
                self.counter += 1
                self.curMinute = datetime(tickTime.year, tickTime.month, tickTime.day, tickTime.hour, tickTime.minute)
                self.open = quote.NewPrice
                self.volume = 0
                self.amount = 0
                self.high = 0
                self.low = 9999999999
                self.upperLimit = 0
                self.lowerLimit = 0
            else:
                self.high = quote.NewPrice if quote.NewPrice > self.high else self.high
                self.low = quote.NewPrice if quote.NewPrice < self.low else self.low
                self.close  = quote.NewPrice
                self.time = quote.TickTime
                self.volume += quote.TickVolume
                self.amount += quote.TickAmount
                self.upperLimit = quote.UpperLimit
                self.lowerLimit = quote.LowerLimit

    def save(self, savePath):
        self.data.to_csv(savePath)          

if __name__ == "__main__":
    gen = tickQuote("./backTestData/tickMore")
    myKLine = KLine(minutes=1, datalength=200)  # 1min 的k线 除了开盘时候的成交量，其余基本大小都正确
    while True:
        try:
            a = next(gen)
            # print(a.TickTime)
            tickTime = datetime.strptime(a.TickTime, "%Y%m%d.%H:%M:%S.%f")
            myKLine.update(a)
        except Exception as e:
            print(f"读取tick行情结束, {e}")
            break
        # if len(myKLine.data) > 20:
        #     print(myKLine.data.tail(21))
        #     break
    print(myKLine.data.tail(200))

    