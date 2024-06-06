

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
                    'vol': int,  # 手数
                    'direction': utils.orderDirection,  # 方向
                    'openAvgPrice': float, # 开仓均价
                    'PL': float   # 盈亏
                }
            }
        """


