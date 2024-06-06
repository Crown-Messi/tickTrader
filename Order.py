
import utils
from typing import List

class Order(object):
    order_ID = 0
    orderList = []  # [order]
    def __init__(self, time:str, code:str, vol:int, price:float, direction:int, state:int):
        self.time       = time
        self.code       = code
        self.vol        = vol
        
        self.price      = price
        self.direction  = direction  # utils.orderDirection
        self.state      = state      # utils.orderState
        self.orderID    = Order.order_ID

        self.dealVol    = []  # 成交信息
        self.dealPrice  = [] 
