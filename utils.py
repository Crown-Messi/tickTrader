import enum
from Order import Order
from Account import Account

# 订单状态         全成    部成   全撤  部撤  等待成交（已报单）  废单
orderState = enum.Enum("orderState", ("WAITINGREPORT","ALLFINISHED", "PARTFINISHED", "ALLCANCEL", "PARTCANCEL", "WAITINGFINISH", "DISCARD"))

# 订单方向
orderDirection = enum.Enum("orderDirection", ("SHORT_OPEN", "LONG_OPEN", "SHORT_CLOSE", "LONG_CLOSE", "CANCEL"))

# 错误代码
Error = enum.Enum("Error", ("error1", "error2","error3"))


# 撤单代码
Cancel = enum.Enum("Cancel", ("cancel1", "cancel2", "cancel3"))

errorDict = {
    1:"Invalid order - trade himself.",
    2:"Invalid order - have not enough volumes.",
    3:"Available money is not enough.",
    4:"Unreasonable price, bigger than upper limit or smaller than lower limit."
}


cancelDict = {
    1:"Time is over but order can not been dealt.",  # 撤单时间到，订单未成交
    2:"Invaild order - trade himself during dealing.", 
    3:"Invalid order - order does not exist."
}


def printOrder(order:Order):
    print(f"Order info: \n {'------'*8}")
    print(f"\t\t 编号：{order.orderID} \n\
            \t 时间：{order.time} \n \
            \t 品种：{order.code} \n\
            \t 方向：{order.direction} \n\
            \t 价格：{order.price} \n\
            \t 手数：{order.vol} \n\
            \t 状态：{order.state} \n\
            {'------'*8}")
    
def printOrderList(order:Order):
    print("Order List:")
    for od in Order.orderList:
        print(f"\t {od.orderID}")

def printAccount(account:Account):
    print(f"账户信息：\n {'^^^'*3}")
    print(f"\t\t 资产：{account.asset} \n \
            \t 可用资金：{account.available} \n \
            \t 资金使用率：{account.useRate} \n \
            \t 仓位：{account.position} \n \
            \t 历史订单：{account.historyOrder} \n\
            {'^^^'*3}")
    pass

class response():
    def __init__(self, msg, order, account):
        self.msg     = msg # 回报中显示的单子状态
        self.m_order = order 
        self.account = account