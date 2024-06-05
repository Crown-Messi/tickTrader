
from order import Order
import utils
from account import Account
from  quote import Quote


class response():
    def __init__(self):
        self.m_status: str # 回报中显示的单子状态
        self.m_order: Order 


class CallBackBase(object):
    def __init__(self):
        pass

    def respOrderSendCallBack(self, resp:response, order:Order):
        
        """
        发单回报
        """
        pass

    def respOrderDealCallBack(self, resp:response, order:Order, quote: Quote):
        """
        成交回报
        """
        pass

    def respOrderCancelCallBack(self, resp:response, order:Order):
        """
        撤单回报
        """
        pass


class smltCallBack(CallBackBase):
    def __init__(self, account: Account):
        super(smltCallBack, self).__init__()
        self.account = account
    
    def respOrderSendCallBack(self, resp:response, order:Order):
        """
        发单回报
        """
        print("发单：")
        order.orderList.append(order)
        utils.printOrder(order)
        pass

    def respOrderDealCallBack(self, resp:response, order:Order,  quote: Quote):
        """
        成交回报
        """
        print("订单成交：")
        if order.direction == utils.orderDirection.LONG_CLOSE or order.direction == utils.orderDirection.SHORT_CLOSE:
            preOrder = [od for od in order.orderList if od.code] # 此时的orderlist已经经过了风控模块，订单不会出现问题
            
            # if order.vol == 
            # order.orderList.remove(order)
            
    
        self.account.position[order.code] = {
            "position": order.direction,
            "price": order.price,
            "volume": order.vol, 
            "dealTime": quote.TickTime
        }
        pass

    def respOrderCancelCallBack(self, resp:response, order:Order):
        """
        撤单回报
        """
        print("撤单")
        order.orderList.remove(order)

        pass