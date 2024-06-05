
import utils


class Order(object):
    order_ID = 0
    def __init__(self, time:str, code:str, vol:int, price:float, direction:int, state:int):
        self.time       = time
        self.code       = code
        self.vol        = vol
        self.price      = price
        self.direction  = direction  # utils.orderDirection
        self.state      = state      # utils.orderState
        self.orderID    = Order.order_ID
