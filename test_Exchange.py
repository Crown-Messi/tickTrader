from config import parse_args
from Exchange import Exchange
from Account import Account
from smltCallBack import smltCallBack
from base_strategy import myStrategy


if __name__ == "__main__":
    args = parse_args()
    args.account = Account(asset=1e6)
    args.callback = smltCallBack(args)
    ex = Exchange(args)

    mystg = {
        "KLine": 1, 
        "KLineLength": 100,
        "stgFunction": myStrategy,
        "cancelSeconds":60
    }

    ex.makeBackTest(mystg)
    

