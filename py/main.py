from utils import *
from tx_sender import send_tx
import os, time, datetime, json

def single_trade():
    denom = "uosmo"
    tx_fee = 2000
    min_amount = tx_fee
    max_hop = 3
    iter = 10

    time_a = time.time()
    print("Starting process at", datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
    address = os.getenv("OSADDRESS")
    balace = get_balance(address, denom)
    print("balance = ", balace, denom)
    options = {"denom": "uosmo", "max_hop": max_hop, "iter":iter, "min_amount":min_amount, "max_amount":balace}
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
    print("profit = ", profit)
    if profit > 1.1*tx_fee:
        print("Sending transaction...")
        result = send_tx(trade, tx_fee)
        time_d = time.time()
        print("Done in ", time_d - time_c, "sec.")
        balace_after = get_balance(address, denom)
        print("balance after is ", balace_after)
        print("Actual profit was", balace_after - balace)
    else:
        print("Should not trade.")

def trade_loop():
    while True:
        try:
            single_trade()
            time.sleep(30)
        except:
            print("Exception occurred")

trade_loop()