import requests
import subprocess
import json, time

lcd = "https://lcd-osmosis.blockapsis.com"
lcd = "https://osmosis.stakesystems.io"

def get_pool_str():
    Pools = []
    pagination = ""
    while pagination!=None:
        pools = requests.get(lcd + "/osmosis/gamm/v1beta1/pools"+"?pagination.key="+pagination).json()
        Pools.extend(pools["pools"])
        pagination = pools["pagination"]["next_key"]
        # time.sleep(0.1)

    Pools_formatted = []
    for pool in Pools:
        id = int(pool["id"])
        swap_fee = float(pool["poolParams"]["swapFee"])
        coin0 = pool["poolAssets"][0]
        weight0 = int(coin0["weight"])
        token0 = coin0["token"]
        denom0 = token0["denom"]
        amount0 = int(token0["amount"])

        coin1 = pool["poolAssets"][1]
        weight1 = int(coin1["weight"])
        token1 = coin1["token"]
        denom1 = token1["denom"]
        amount1 = int(token1["amount"])
        pool_formatted = {  "id": id, \
                            "swap_fee": swap_fee,\
                            "denom0":denom0,\
                            "amount0":amount0,\
                            "weight0":weight0, \
                            "denom1":denom1, \
                            "amount1":amount1, \
                            "weight1":weight1}
        Pools_formatted.append(pool_formatted)
    return json.dumps(Pools_formatted)

def execute_main(pools_str, options_str):
    result = subprocess.run(["./target/release/main", pools_str, options_str], capture_output=True, text=True)
    trade =  json.loads(result.stdout.split("\n")[0])
    return trade


def make_pools():
    with open("pools.json", "w") as f:
        f.write(get_pool_str())

def get_balance(address, denom):
    res = requests.get(lcd + "/cosmos/bank/v1beta1/balances/" + address).json()
    for coin in res["balances"]:
        if coin["denom"]==denom:
            return int(coin["amount"])

# struct Option{
#     pub denom: String,
#     pub max_hop: usize,
#     pub iter: i32,
#     pub min_amount: i128,
#     pub max_amount: i128,
# }


# pub struct Pool{
    # id: u32, 
#     swap_fee: f64,
#     denom0: String,
#     amount0: i128,
#     weight0: i128,
#     denom1: String,
#     amount1: i128,
#     weight1: i128,
# }



# {"@type&": "/osmosis.gamm.v1beta1.Pool",
#   "address": "osmo1s666n6f6qhw2hcgkmwx3jxl7hz35cytrygmcvzcxxt84e8nrjfus4wyknj"&,
#    "id": "739",
#     "poolParams": {"swapFee": "0.000000000000000000",
#      "exitFee": "0.000000000000000000",
#       "smoothWeightChangeParams": null},
#        "future_pool_governor": "24h",
#         "totalShares": {"denom": "gamm/pool/739", "amount":  "100000000000000000000"}, 
#         "poolAssets": [{"token": {"denom": "ibc/0CD3A0285E1341859B5E86B6AB7682F023D03E97607CCC1DC95706411D866DF7", "amount": "883025025496879662"}, "weight": "536870912000000"}, {"token": {"denom": "ibc/D189335C6E4A68B513C10AB227BF1C1D38C746766278BA3EEB4FB14124F1D858", "amount": "882035"}, "weight": "536870912000000"}],
#          "totalWeight": "1073741824000000"}