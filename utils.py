import enum
from order import Order

# 订单状态
orderState = enum.Enum("orderState", ("ALLFINISHED", "PARTFINISHED", "ALLBACK", "WAITINGFINISH", "DISCARD"))

# 订单方向
orderDirection = enum.Enum("orderDirection", ("SHORT_OPEN", "LONG_OPEN", "SHORT_CLOSE", "LONG_CLOSE"))

# 错误代码
Error = enum.Enum("Error", ("error1", "error2","error3"))

errorDict = {
    1:"Invalid order - trade himself",
    2:"Invalid order - have not enough volumes",
    3:"Available money is not enough",
    4:"Unreasonable price, bigger than upper limit or smaller than lower limit."
}


def printOrder(order:Order):
    print(f"Order info: \n {'------'*8}")
    print(f"\t {order.order_ID} \n\
            \t {order.orderID} \n\
            \t {order.time} \n \
            \t {order.code} \n\
            \t {order.direction} \n\
            \t {order.price} \n\
            \t {order.vol} \n\
            {'------'*8}")