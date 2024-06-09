
from Account import Account
from Order import Order
from Quote import Quote, tickQuote, KLine
import utils
from utils import response


class Exchange(object):
    def __init__(self, args) -> None:
        self.KLine = None
        self.args = args
        self.gen = tickQuote(args.tickDataSource)

    def makeBackTest(self, strategy:dict):
        """
        strategy: dict
        {
            KLine: -1,   # 该参数为-1，表示策略是基于tick行情的，正数表示策略是基于对应分钟的K线
            KLineLength: 0, # 测
            stgFunction: 开仓策略函数（基于tick的策略还没有开发过）
            cancelSeconds: 撤单的秒数，如果是基于K线撤单的，该参数应该置为-1

        }
        """
        STGKLine = strategy["KLine"]
        STGFunc = strategy["stgFunction"]
        STGCancel = strategy["cancelSeconds"]
        
        if STGKLine > 0:
            self.KLine = KLine(minutes=STGKLine, datalength=strategy["KLineLength"])  # 本质上是一个pandas 的DataFrame对象
            while True:
                try:
                    rightTick = next(self.gen)
                    
                    
                    
                    
                    if self.KLine.update(rightTick):
                        STGFunc(self.KLine)  # K线更新 策略执行
                        stg = self.KLine.iloc[-1]
                        if STGCancel != -1:  # 基于k线的撤单函数
                            if self.KLine.iloc[-1].tradingFlag == utils.orderDirection.CANCEL:
                                for od in Order.orderList:
                                    if od.code == stg.code:                       
                                        self.checkCancel(od, self.args.account, self.args.callback.respOrderCancelCallBack, rightTick)
                        
                        # 如果产生发单信号，则生成订单并进行风控检查
                        if stg.tradingFlag == utils.orderDirection.LONG_OPEN or stg.tradingFlag == utils.orderDirection.SHORT_OPEN:
                            order = Order(time=stg.time, code=stg.code, vol=stg.tradingVol, price=stg.tradingPrice, direction=stg.tradingFlag, state=utils.orderState.WAITINGREPORT)
                            self.riskControl(account=self.args.account, order=order, quote=rightTick, callback=self.args.callback.respOrderSendCallBack)
                        
                    # 当前tick的成交检查
                    self.checkDeal(quote=rightTick, quickDeal=self.args.quickDeal,account=self.args.account, callBack=self.args.callback.respOrderDealCallBack)
                    # 当前tick的止盈止损线检查

                    
                    
                        


                    
                except Exception as e:
                    print(f"读取tick行情结束, {e}")
        else:
            while True:
                try:
                    pass
                except:
                    pass


    def riskControl(self, account:Account, order:Order, quote:Quote, callback:function) -> int:
        """ 检查订单是否合法：
            - 可用资金是否充足
            - 自成交检查
        """
        if order.code in account.position:
            # 自成交
            if (order.direction == utils.orderDirection.LONG_OPEN and account.position[order.code]["direction"] == utils.orderDirection.SHORT_OPEN) or \
                (order.direction == utils.orderDirection.SHORT_OPEN and account.position[order.code]["direction"] == utils.orderDirection.LONG_OPEN):
                return utils.Error.error1

            # 平仓手数不足
            if order.direction == utils.orderDirection.SHORT_CLOSE or order.direction == utils.orderDirection.LONG_CLOSE and order.vol > account.position["order.code"]["vol"]:
                return utils.Error.error2
            
            # 开仓可用资金不足
            if order.direction == utils.orderDirection.LONG_OPEN or order.direction == utils.orderDirection.SHORT_OPEN and account.available < order.price*order.vol*quote.LotNumber*quote.MarginRate:
                return utils.Error.error3

        if order.code == quote.Instrument + "." + quote.ExCode: 
            # 价格过滤
            if order.price > quote.UpperLimit or order.price < quote.LowerLimit:
                return utils.Error.error4
        

        account.available -= order.vol*order.price*quote.LotNumber*quote.MarginRate
        order.orderList.append(order)
        account.historyOrder.append(order)

        order.state = utils.orderState.WAITINGFINISH
        
        callback(response("订单发送", order))
        
        return 0


    def checkDeal(self, quote:Quote, quickDeal:bool, account:Account, callBack:function):
        """判断订单在tick状态下是否可以成交
        Args:
            order：订单对象，主要是需要订单类的属性 orderList
            quote：tick行情
            quickDeal：回测是否需要立即成交，不立即成交的话采用何种策略（未开发）
            account：账户
            callBack：成交的回报函数对象
        """
        for od in Order.orderList:
            if not self.riskControl(account, od, quote, self.args.callback.respOrderSendCallBack):
                pass
            else:
                self.checkCancel(od, account, self.args.callback.respOrderCancelCallBack, quote) # 同一品种的反向订单可以开出来，但是只要有其中一个订单成交了的话，另一个订单相当于是自成交，被判定后自动撤单

            # 同一标的有多个订单
            if quickDeal:
                if od.direction == utils.orderDirection.LONG_CLOSE or od.direction == utils.orderDirection.SHORT_OPEN:
                    if quote.BuyPrice1 >= od.price:
                        od.dealVol.append(min(quote.BuyVolume1, od.vol))
                        od.dealPrice.append(min(quote.BuyPrice1, od.price))
                        od.vol = od.vol - od.dealVol[-1]
                        account.available += od.dealVol[-1]*od.dealPrice[-1]*quote.LotNumber*quote.MarginRate
                        
                        if quote.TwoSideFee:  # 有的品种是双边手续费
                            account.available -= od.dealVol[-1]*quote.Fee
                        
                        account.position[od.code] = {
                            "position": od.direction,
                            "price": od.price,
                            "volume": od.vol, 
                            "dealTime": quote.TickTime
                        }
                        if od.vol != 0:
                            od.status = utils.orderState.PARTFINISHED
                        else:
                            od.status = utils.orderState.ALLFINISHED
                            Order.orderList.remove(od)
                        
                        callBack(response("成交回报", od))
                elif od.direction == utils.orderDirection.LONG_OPEN or od.direction == utils.orderDirection.SHORT_CLOSE:
                    if quote.AskPrice1 <= od.price:
                        od.dealVol.append(min(quote.AskVolume1, od.vol))
                        od.dealPrice.append(min(quote.AskPrice1, od.price))
                        od.vol = od.vol - od.dealVol[-1]
                        account.available -= (od.dealVol[-1]*od.dealPrice[-1]*quote.LotNumber*quote.MarginRate + od.dealPrice[-1]*quote.Fee)
                        account.position[od.code] = {
                            "position": od.direction,
                            "price": od.price,
                            "volume": od.vol, 
                            "dealTime": quote.TickTime
                        }
                        
                        if od.vol != 0:
                            od.status = utils.orderState.PARTFINISHED
                        else:
                            od.status = utils.orderState.ALLFINISHED
                            Order.orderList.remove(od)
                        
                        callBack(response("成交回报", od))
            else:
                pass


    def checkCancel(self, order:Order, account:Account, callBack:function, quote:Quote):
        """撤单检查
        Args:
            order：目标撤销订单
            callBack：回调函数
        """
        if order not in order.orderList:
            callBack(response("撤单失败，订单不存在", order))
            return 

        order.orderList.remove(order)
        account.available += order.vol*order.price*quote.LotNumber*quote.MarginRate
        if order.dealVol != 0:
            order.state = utils.orderState.PARTCANCEL
        else:
            order.state = utils.orderState.ALLCANCEL
        
        callBack(response("撤单回报", order))