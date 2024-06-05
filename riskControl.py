
from .account import Account
from .order import Order
from .quote import Quote
import utils



"""
检查订单是否合理：
    可用资金是否充足
    自成交检查
"""
def riskControl(account:Account, order:Order, quote:Quote) -> int:

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
        
    return 0


def judgeDeal(order:Order, quote:Quote):
    """
    判断订单在tick状态下是否可以成交
    成交的话需要回调成交回报函数
    """
    for od in order.orderList:
        pass