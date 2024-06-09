from config import parse_args
from Exchange import Exchange
from Account import Account
from smltCallBack import smltCallBack

if __name__ == "__main__":
    args = parse_args()
    args.account = Account(asset=1e6)
    args.callback = smltCallBack()
    ex = Exchange(args)