
from .account import Account
from .order import Order
from .quote import Quote
import utils
from utils import response


"""
检查订单是否合理：
    可用资金是否充足
    自成交检查
"""
def riskControl(account:Account, order:Order, quote:Quote, callback:function) -> int:

    if order.code in account.position:
        # 自成交
        if (order.direction == utils.orderDirection.LONG_OPEN and account.position[order.code]["direction"] == utils.orderDirection.SHORT_OPEN) or \
            (order.direction == utils.orderDirection.SHORT_OPEN and account.position[order.code]["direction"] == utils.orderDirection.LONG_OPEN):
            return utils.Error.error1
        
        # 平仓手数不足
        if order.direction == utils.orderDirection.SHORT_CLOSE or order.direction == utils.orderDirection.LONG_CLOSE and order.vol > account.position["order.code"]["vol"]:
            return utils.Error.error2
        
        # 开仓可用资金不足
        if order.direction == utils.orderDirection.LONG_OPEN or order.direction == utils.orderDirection.SHORT_OPEN and account.available < order.price*order.vol:
            return utils.Error.error3

    if order.code == quote.Instrument + "." + quote.ExCode: 
        # 价格过滤
        if order.price > quote.UpperLimit or order.price < quote.LowerLimit:
            return utils.Error.error4
    
    order.orderList.append(order)
    account.historyOrder.append(order)
    order.state = utils.orderState.WAITINGFINISH
    
    callback(response("订单发送", order))
    
    return 0


def checkDeal(order:Order, quote:Quote, quickDeal:bool, account:Account, callBack:function):
    """判断订单在tick状态下是否可以成交
    Args:
        order：订单对象，主要是需要订单类的属性 orderList
        quote：tick行情
        quickDeal：回测是否需要立即成交，不立即成交的话采用何种策略（未开发）
        account：账户
        callBack：成交的回报函数对象
    """
    for od in order.orderList:
        # 同一标的有多个订单
        if quickDeal:
            if od.direction == utils.orderDirection.LONG_CLOSE or od.direction == utils.orderDirection.SHORT_OPEN:
                if quote.BuyPrice1 >= od.price:
                    od.dealVol.append(min(quote.BuyVolume1, od.vol))
                    od.dealPrice.append(min(quote.BuyPrice1, od.price))
                    od.vol = od.vol - od.dealVol[-1]
                    account.available += od.dealVol[-1]*od.dealPrice[-1]
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
                        order.orderList.remove(od)
            elif od.direction == utils.orderDirection.LONG_OPEN or od.direction == utils.orderDirection.SHORT_CLOSE:
                if quote.AskPrice1 <= od.price:
                    od.dealVol.append(min(quote.AskVolume1, od.vol))
                    od.dealPrice.append(min(quote.AskPrice1, od.price))
                    od.vol = od.vol - od.dealVol[-1]
                    account.available -= od.dealVol[-1]*od.dealPrice[-1]
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
                        order.orderList.remove(od)
        else:
            pass

        callBack(response("成交回报", od))



def checkCancel(order:Order, account:Account, callBack:function):
    pass