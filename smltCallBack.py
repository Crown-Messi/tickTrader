
from Order import Order
import utils
from Account import Account
from  Quote import Quote
from utils import response




class CallBackBase(object):
    def __init__(self):
        pass

    def respOrderSendCallBack(self, resp:response):
        
        """
        发单回报
        """
        pass

    def respOrderDealCallBack(self, resp:response):
        """
        成交回报
        """
        pass

    def respOrderCancelCallBack(self, resp:response):
        """
        撤单回报
        """
        pass


class smltCallBack(CallBackBase):
    def __init__(self, args):
        super(smltCallBack, self).__init__()
        self.args = args
    
    def respOrderSendCallBack(self, resp:response):
        """
        发单回报
        """
        print("发单：")
        utils.printOrder(resp.m_order)
        

    def respOrderDealCallBack(self, resp:response):
        """
        成交回报
        """
        print("成交")
        utils.printOrder(resp.m_order)

    def respOrderCancelCallBack(self, resp:response):
        """
        撤单回报
        """
        print("撤单")
        utils.printOrder(resp.m_order)