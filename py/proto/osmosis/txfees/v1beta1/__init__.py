# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: osmosis/txfees/v1beta1/feetoken.proto, osmosis/txfees/v1beta1/genesis.proto, osmosis/txfees/v1beta1/gov.proto, osmosis/txfees/v1beta1/query.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import Dict, List

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase
import grpclib


@dataclass(eq=False, repr=False)
class FeeToken(betterproto.Message):
    """
    FeeToken is a struct that specifies a coin denom, and pool ID pair. This
    marks the token as eligible for use as a tx fee asset in Osmosis. Its price
    in osmo is derived through looking at the provided pool ID. The pool ID
    must have osmo as one of its assets.
    """

    denom: str = betterproto.string_field(1)
    pool_id: int = betterproto.uint64_field(2)


@dataclass(eq=False, repr=False)
class UpdateFeeTokenProposal(betterproto.Message):
    """
    UpdateFeeTokenProposal is a gov Content type for adding a new whitelisted
    fee token. It must specify a denom along with gamm pool ID to use as a spot
    price calculator. It can be used to add a new denom to the whitelist It can
    also be used to update the Pool to associate with the denom. If Pool ID is
    set to 0, it will remove the denom from the whitelisted set.
    """

    title: str = betterproto.string_field(1)
    description: str = betterproto.string_field(2)
    feetoken: "FeeToken" = betterproto.message_field(3)


@dataclass(eq=False, repr=False)
class QueryFeeTokensRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class QueryFeeTokensResponse(betterproto.Message):
    fee_tokens: List["FeeToken"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class QueryDenomSpotPriceRequest(betterproto.Message):
    """
    QueryDenomSpotPriceRequest defines grpc request structure for querying spot
    price for the specified tx fee denom
    """

    denom: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class QueryDenomSpotPriceResponse(betterproto.Message):
    """
    QueryDenomSpotPriceRequest defines grpc response structure for querying
    spot price for the specified tx fee denom
    """

    pool_id: int = betterproto.uint64_field(1)
    spot_price: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class QueryDenomPoolIdRequest(betterproto.Message):
    denom: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class QueryDenomPoolIdResponse(betterproto.Message):
    pool_id: int = betterproto.uint64_field(1)


@dataclass(eq=False, repr=False)
class QueryBaseDenomRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class QueryBaseDenomResponse(betterproto.Message):
    base_denom: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class GenesisState(betterproto.Message):
    """GenesisState defines the txfees module's genesis state."""

    basedenom: str = betterproto.string_field(1)
    feetokens: List["FeeToken"] = betterproto.message_field(2)


class QueryStub(betterproto.ServiceStub):
    async def fee_tokens(self) -> "QueryFeeTokensResponse":

        request = QueryFeeTokensRequest()

        return await self._unary_unary(
            "/osmosis.txfees.v1beta1.Query/FeeTokens", request, QueryFeeTokensResponse
        )

    async def denom_spot_price(
        self, *, denom: str = ""
    ) -> "QueryDenomSpotPriceResponse":

        request = QueryDenomSpotPriceRequest()
        request.denom = denom

        return await self._unary_unary(
            "/osmosis.txfees.v1beta1.Query/DenomSpotPrice",
            request,
            QueryDenomSpotPriceResponse,
        )

    async def denom_pool_id(self, *, denom: str = "") -> "QueryDenomPoolIdResponse":

        request = QueryDenomPoolIdRequest()
        request.denom = denom

        return await self._unary_unary(
            "/osmosis.txfees.v1beta1.Query/DenomPoolId",
            request,
            QueryDenomPoolIdResponse,
        )

    async def base_denom(self) -> "QueryBaseDenomResponse":

        request = QueryBaseDenomRequest()

        return await self._unary_unary(
            "/osmosis.txfees.v1beta1.Query/BaseDenom", request, QueryBaseDenomResponse
        )


class QueryBase(ServiceBase):
    async def fee_tokens(self) -> "QueryFeeTokensResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def denom_spot_price(self, denom: str) -> "QueryDenomSpotPriceResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def denom_pool_id(self, denom: str) -> "QueryDenomPoolIdResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def base_denom(self) -> "QueryBaseDenomResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_fee_tokens(self, stream: grpclib.server.Stream) -> None:
        request = await stream.recv_message()

        request_kwargs = {}

        response = await self.fee_tokens(**request_kwargs)
        await stream.send_message(response)

    async def __rpc_denom_spot_price(self, stream: grpclib.server.Stream) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "denom": request.denom,
        }

        response = await self.denom_spot_price(**request_kwargs)
        await stream.send_message(response)

    async def __rpc_denom_pool_id(self, stream: grpclib.server.Stream) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "denom": request.denom,
        }

        response = await self.denom_pool_id(**request_kwargs)
        await stream.send_message(response)

    async def __rpc_base_denom(self, stream: grpclib.server.Stream) -> None:
        request = await stream.recv_message()

        request_kwargs = {}

        response = await self.base_denom(**request_kwargs)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/osmosis.txfees.v1beta1.Query/FeeTokens": grpclib.const.Handler(
                self.__rpc_fee_tokens,
                grpclib.const.Cardinality.UNARY_UNARY,
                QueryFeeTokensRequest,
                QueryFeeTokensResponse,
            ),
            "/osmosis.txfees.v1beta1.Query/DenomSpotPrice": grpclib.const.Handler(
                self.__rpc_denom_spot_price,
                grpclib.const.Cardinality.UNARY_UNARY,
                QueryDenomSpotPriceRequest,
                QueryDenomSpotPriceResponse,
            ),
            "/osmosis.txfees.v1beta1.Query/DenomPoolId": grpclib.const.Handler(
                self.__rpc_denom_pool_id,
                grpclib.const.Cardinality.UNARY_UNARY,
                QueryDenomPoolIdRequest,
                QueryDenomPoolIdResponse,
            ),
            "/osmosis.txfees.v1beta1.Query/BaseDenom": grpclib.const.Handler(
                self.__rpc_base_denom,
                grpclib.const.Cardinality.UNARY_UNARY,
                QueryBaseDenomRequest,
                QueryBaseDenomResponse,
            ),
        }
