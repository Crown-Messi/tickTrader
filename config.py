
import argparse


tickDataSource = "./backTestData/tickMore"


def parse_args():
    parse = argparse.ArgumentParser(description="期货回测tick回测成交系统参数")
    parse.add_argument("tickDataSource", default="/home/ztcapital/Codes/FutureQuant/backTestData/tickMore", type=str, help="tick行情数据目录，数据是一档存在，二到五档空")
    parse.add_argument("KLine", default=1, type=int, help="K线级别")
    parse.add_argument("KLineLength", default=100, type=int, help="策略应用K线的长度")
    args = parse.parse_args()

    return args
