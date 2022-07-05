from __future__ import annotations

from terra_sdk.key.mnemonic import MnemonicKey
from terra_sdk.client.lcd import LCDClient
from terra_sdk.client.lcd.api.tx import CreateTxOptions
from terra_sdk.core.fee import Fee
import base64

import attr
from terra_sdk.core.msg import Msg
from terra_proto.cosmos.bank.v1beta1 import MsgSend as MsgSend_pb
from terra_sdk.core import AccAddress, Coins, Coin

from proto.osmosis.gamm.v1beta1 import MsgSwapExactAmountIn as MsgSwapExactAmountIn_pb
from proto.osmosis.gamm.v1beta1 import SwapAmountInRoute as SwapAmountInRoute_pb
from typing import Any, Callable, Dict, Iterable, Iterator, List, Optional, Union

import os

@attr.s
class MsgSend(Msg):
    """Sends native Terra assets (Luna or Terra stablecoins) from ``from_address`` to ``to_address``.

    Args:
        from_address (AccAddress): sender
        to_address (AccAddress): recipient
        amount (Coins): coins to send
    """

    type_amino = "cosmos-sdk/MsgSend"
    """"""
    type_url = "/cosmos.bank.v1beta1.MsgSend"
    """"""
    action = "send"
    """"""
    prototype = MsgSend_pb
    """"""

    from_address: AccAddress = attr.ib()
    to_address: AccAddress = attr.ib()
    amount: Coins = attr.ib(converter=Coins)

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "from_address": self.from_address,
                "to_address": self.to_address,
                "amount": self.amount.to_amino(),
            },
        }

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "from_address": self.from_address,
            "to_address": self.to_address,
            "amount": self.amount.to_data(),
        }

    def to_proto(self) -> MsgSend_pb:
        proto = MsgSend_pb()
        proto.from_address = self.from_address
        proto.to_address = self.to_address
        proto.amount = [c.to_proto() for c in self.amount]
        return proto

@attr.s
class MsgSwapExactAmountIn(Msg):
    """swap coins.

    Args:
        from_address (AccAddress): sender
        to_address (AccAddress): recipient
        amount (Coins): coins to send
    """

    # type_amino = "cosmos-sdk/MsgSend"
    """"""
    type_url = "/osmosis.gamm.v1beta1.MsgSwapExactAmountIn"
    """"""
    action = "swap"
    """"""
    prototype = MsgSwapExactAmountIn_pb
    """"""

    sender: AccAddress = attr.ib()
    routes: List[dict] = attr.ib()
    token_in: Coin = attr.ib()
    token_out_min_amount: str = attr.ib()

    def to_proto(self) -> MsgSwapExactAmountIn_pb:
        
        proto = MsgSwapExactAmountIn_pb()
        proto.sender = self.sender
        for route in self.routes:
            proto_route = SwapAmountInRoute_pb()
            proto_route.pool_id = int(route["pool_id"])
            proto_route.token_out_denom = route["token_out_denom"]
            proto.routes.append(proto_route)
        proto.token_in = self.token_in.to_proto()
        proto.token_out_min_amount = self.token_out_min_amount
        return proto

def send_tx(trade, tx_fee):
    mk = MnemonicKey(mnemonic=os.getenv("MNEMONIC"))
    terra = LCDClient("https://lcd-osmosis.blockapsis.com", "osmosis-1")
    address = os.getenv("OSADDRESS")
    wallet = terra.wallet(mk)
    msgswap = MsgSwapExactAmountIn(sender=address, \
    routes = trade["routes"],\
        token_in = Coin.from_str(str(trade["token_in_amount"])+trade["token_in_denom"] ), \
        token_out_min_amount=str(trade["token_in_amount"]))

    tx = wallet.create_and_sign_tx(CreateTxOptions(
        msgs=[msgswap],
        memo="",
        fee=Fee(400000, str(tx_fee) +  "uosmo")
    ))
    result = terra.tx.broadcast(tx)
    return result

