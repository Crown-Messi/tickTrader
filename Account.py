

class Account(object):
    def __init__(self, asset=1e6) -> None:
        self.asset = asset
        self.available = self.asset
        self.useRate = 0
        self.position = {}
        self.historyOrder = []
        """
            {
                'future code':
                {
                    'volume': int,  # 手数  空开为负数
                    'lockVol': int,
                    'amount':float
                    'direction': utils.orderDirection,  # 方向
                    'openAvgPrice': float, # 开仓均价
                    'PL': float   # 盈亏
                    'stopEarnLoss':[[orderid, suborderid, direction, vol, earnPrice, lossPrice, closeOrderID]]
                    'dealtime':str
                }
            }
        """


