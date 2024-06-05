
from order import Order


class response():
    def __init__(self):
        self.m_status: str # 回报中显示的单子状态
        self.m_order: Order 





class smltCallBackBase(object):
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


class smltCallBack(smltCallBackBase):
    def __init__(self):
        super(smltCallBack, self).__init__()