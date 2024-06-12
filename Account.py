

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
                    'volume': int,  # 手数
                    'amount':float
                    'direction': utils.orderDirection,  # 方向
                    'openAvgPrice': float, # 开仓均价
                    'PL': float   # 盈亏
                    'stopEarnLoss':[[direction, vol, price]]
                    'dealtime':str
                }
            }
        """


