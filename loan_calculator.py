import math
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--type")
parser.add_argument("--principal", type=int)
parser.add_argument("--payment", type=int)
parser.add_argument("--periods", type=int)
parser.add_argument("--interest", type=float)
args = parser.parse_args()
listA, sum, res = [], 0, 0
for arg in vars(args):
    if getattr(args, arg) is not None:
        listA.append(getattr(args, arg))
if args.interest is None or args.type not in ("diff", "annuity") or len(listA) != 4:
    print("Incorrect parameters")
elif args.type == "diff" and args.principal is not None and args.periods is not None:
    for i in range(1, args.periods + 1):
        x = (args.interest / 1200) * (args.principal - (args.principal * (i - 1)) / args.periods)
        y = (args.principal / args.periods)
        res = y + x
        print(f"Month {i}: payment is {math.ceil(res)}")
        sum += (math.ceil(res) - y)
    print("Overpayment =", round(sum))
elif args.type == "annuity" and args.payment is not None and args.periods is not None:
    x = args.interest / 1200
    y = (x * math.pow(1 + x, args.periods)) / (math.pow(1 + x, args.periods) - 1)
    res = args.payment / y
    print(f"Your loan principal = {math.floor(res)}!")
    for i in range(1, args.periods + 1):
        sum += args.payment
    print(f"Overpayment = {sum - math.floor(res)}")
elif args.type == "annuity" and args.principal is not None and args.payment is not None:
    x = args.interest / 1200
    n = args.payment / (args.payment - x * args.principal)
    repay = math.ceil(math.log(n, x + 1))
    years = repay // 12
    months = repay % 12
    if years != 0 and months != 0:
        print(f'It will take {years} years and {months} months to repay this loan!')
    elif years == 0:
        print(f'It will take {months} months to repay this loan!')
    elif months == 0:
        print(f'It will take {years} years to repay this loan!')
    print(f"Overpayment = {(repay * args.payment) - args.principal}")
elif args.type == "annuity" and args.principal is not None and args.periods is not None:
    i = args.interest / 1200
    x = i * math.pow(1 + i, args.periods)
    y = math.pow(1 + i, args.periods) - 1
    res = math.ceil(args.principal * (x / y))
    print(f"Your annuity payment = {res}!")
    print(f"Overpayment = {(res * args.periods) - args.principal}")