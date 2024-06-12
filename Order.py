from typing import List

class Order(object):
    orderList = []  # [order]
    def __init__(self, orderid:int, time:str, code:str, vol:int, price:float, stopEarnPrice:float, stopLossPrice:float, direction:int, state:int):
        self.time           = time
        self.code           = code
        self.vol            = vol
        
        self.price          = price
        self.stopEarnPrice  = stopEarnPrice
        self.stopLossPrice  = stopLossPrice

        self.direction      = direction  # utils.orderDirection
        self.state          = state      # utils.orderState
        self.orderID        = orderid

        self.dealVol        = []  # 成交信息
        self.dealPrice      = [] 
