# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: osmosis/gamm/pool-models/balancer/tx/tx.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import Dict, List, Optional

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase
import grpclib


@dataclass(eq=False, repr=False)
class MsgCreateBalancerPool(betterproto.Message):
    """===================== MsgCreatePool"""

    sender: str = betterproto.string_field(1)
    pool_params: "___v1_beta1__.PoolParams" = betterproto.message_field(2)
    pool_assets: List["___v1_beta1__.PoolAsset"] = betterproto.message_field(3)
    future_pool_governor: str = betterproto.string_field(4)


@dataclass(eq=False, repr=False)
class MsgCreateBalancerPoolResponse(betterproto.Message):
    pool_id: int = betterproto.uint64_field(1)


class MsgStub(betterproto.ServiceStub):
    async def create_balancer_pool(
        self,
        *,
        sender: str = "",
        pool_params: "___v1_beta1__.PoolParams" = None,
        pool_assets: Optional[List["___v1_beta1__.PoolAsset"]] = None,
        future_pool_governor: str = ""
    ) -> "MsgCreateBalancerPoolResponse":
        pool_assets = pool_assets or []

        request = MsgCreateBalancerPool()
        request.sender = sender
        if pool_params is not None:
            request.pool_params = pool_params
        if pool_assets is not None:
            request.pool_assets = pool_assets
        request.future_pool_governor = future_pool_governor

        return await self._unary_unary(
            "/osmosis.gamm.poolmodels.balancer.v1beta1.Msg/CreateBalancerPool",
            request,
            MsgCreateBalancerPoolResponse,
        )


class MsgBase(ServiceBase):
    async def create_balancer_pool(
        self,
        sender: str,
        pool_params: "___v1_beta1__.PoolParams",
        pool_assets: Optional[List["___v1_beta1__.PoolAsset"]],
        future_pool_governor: str,
    ) -> "MsgCreateBalancerPoolResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_create_balancer_pool(self, stream: grpclib.server.Stream) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "sender": request.sender,
            "pool_params": request.pool_params,
            "pool_assets": request.pool_assets,
            "future_pool_governor": request.future_pool_governor,
        }

        response = await self.create_balancer_pool(**request_kwargs)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/osmosis.gamm.poolmodels.balancer.v1beta1.Msg/CreateBalancerPool": grpclib.const.Handler(
                self.__rpc_create_balancer_pool,
                grpclib.const.Cardinality.UNARY_UNARY,
                MsgCreateBalancerPool,
                MsgCreateBalancerPoolResponse,
            ),
        }


from .... import v1beta1 as ___v1_beta1__
