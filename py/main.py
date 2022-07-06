from utils import *
from tx_sender import send_tx
import os, time, datetime, json, pprint

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def single_trade(delta):
    denom = "uosmo"
    tx_fee = 2000
    min_amount = tx_fee
    max_hop = 3
    iter = 50

    time_a = time.time()
    print("Starting process at", datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
    address = os.getenv("OSADDRESS")
    balace = get_balance(address, denom)
    print("balance = ", balace, denom)
    options = {"denom": "uosmo", "max_hop": max_hop, "iter":iter, "min_amount":min_amount, "max_amount":balace - tx_fee}
    options_str = json.dumps(options)
    print("Collecting pools info...")
    pools_str = get_pool_str()
    time_b = time.time()
    print("Done in ", time_b - time_a, "sec.")
    print("Finding trade...")
    trade = execute_main(pools_str, options_str)
    time_c = time.time()
    print("Done in ", time_c - time_b, "sec.")

    profit = trade["profit"]
    pprint.pprint(trade)
    if profit > delta + tx_fee:
        print(f"{bcolors.OKBLUE}Trade route found.{bcolors.ENDC}")
        print("Sending transaction...")
        token_out_min_amount = trade["token_in_amount"]
        result = send_tx(trade, tx_fee, token_out_min_amount)
        time_d = time.time()
        print("Done in ", time_d - time_c, "sec.")
        balace_after = get_balance(address, denom)
        print("balance after is ", balace_after)
        print("Actual profit was", balace_after - balace)
        with open("result.log", "w+") as f:
            print(result, file=f)
        
    else:
        print(f"{bcolors.WARNING}Should not trade.{bcolors.ENDC}")

def trade_loop():
    delta = 100
    while True:
        try:
            single_trade(delta)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(e)

trade_loop()
