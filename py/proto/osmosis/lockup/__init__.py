# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: osmosis/lockup/genesis.proto, osmosis/lockup/lock.proto, osmosis/lockup/query.proto, osmosis/lockup/tx.proto
# plugin: python-betterproto
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase
import grpclib


class LockQueryType(betterproto.Enum):
    # Queries for locks that are longer than a certain duration
    ByDuration = 0
    # Queries for lockups that started before a specific time
    ByTime = 1


@dataclass(eq=False, repr=False)
class PeriodLock(betterproto.Message):
    """
    PeriodLock is a single unit of lock by period. It's a record of locked coin
    at a specific time. It stores owner, duration, unlock time and the amount
    of coins locked.
    """

    id: int = betterproto.uint64_field(1)
    owner: str = betterproto.string_field(2)
    duration: timedelta = betterproto.message_field(3)
    end_time: datetime = betterproto.message_field(4)
    coins: List["__cosmos_base_v1_beta1__.Coin"] = betterproto.message_field(5)


@dataclass(eq=False, repr=False)
class QueryCondition(betterproto.Message):
    # type of lock query, ByLockDuration | ByLockTime
    lock_query_type: "LockQueryType" = betterproto.enum_field(1)
    # What token denomination are we looking for lockups of
    denom: str = betterproto.string_field(2)
    # valid when query condition is ByDuration
    duration: timedelta = betterproto.message_field(3)
    # valid when query condition is ByTime
    timestamp: datetime = betterproto.message_field(4)


@dataclass(eq=False, repr=False)
class SyntheticLock(betterproto.Message):
    """
    SyntheticLock is a single unit of synthetic lockup TODO: Change this to
    have * underlying_lock_id * synthetic_coin * end_time * duration * owner We
    then index synthetic locks by the denom, just like we do with normal locks.
    Ideally we even get an interface, so we can re-use that same logic. I
    currently have no idea how reward distribution is supposed to be working...
    EVENTUALLY we make a "constrained_coin" field, which is what the current
    "coins" field is. Constrained coin field can be a #post-v7 feature, since
    we aren't allowing partial unlocks of synthetic lockups.
    """

    # underlying native lockup id for this synthetic lockup
    underlying_lock_id: int = betterproto.uint64_field(1)
    synth_denom: str = betterproto.string_field(2)
    # used for unbonding synthetic lockups, for active synthetic lockups, this
    # value is set to uninitialized value
    end_time: datetime = betterproto.message_field(3)
    duration: timedelta = betterproto.message_field(4)


@dataclass(eq=False, repr=False)
class MsgLockTokens(betterproto.Message):
    owner: str = betterproto.string_field(1)
    duration: timedelta = betterproto.message_field(2)
    coins: List["__cosmos_base_v1_beta1__.Coin"] = betterproto.message_field(3)


@dataclass(eq=False, repr=False)
class MsgLockTokensResponse(betterproto.Message):
    id: int = betterproto.uint64_field(1)


@dataclass(eq=False, repr=False)
class MsgBeginUnlockingAll(betterproto.Message):
    owner: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class MsgBeginUnlockingAllResponse(betterproto.Message):
    unlocks: List["PeriodLock"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class MsgBeginUnlocking(betterproto.Message):
    owner: str = betterproto.string_field(1)
    id: int = betterproto.uint64_field(2)
    # Amount of unlocking coins. Unlock all if not set.
    coins: List["__cosmos_base_v1_beta1__.Coin"] = betterproto.message_field(3)


@dataclass(eq=False, repr=False)
class MsgBeginUnlockingResponse(betterproto.Message):
    success: bool = betterproto.bool_field(1)


@dataclass(eq=False, repr=False)
class MsgExtendLockup(betterproto.Message):
    """
    MsgExtendLockup extends the existing lockup's duration. The new duration is
    longer than the original.
    """

    owner: str = betterproto.string_field(1)
    id: int = betterproto.uint64_field(2)
    # duration to be set. fails if lower than the current duration, or is
    # unlocking
    duration: timedelta = betterproto.message_field(3)


@dataclass(eq=False, repr=False)
class MsgExtendLockupResponse(betterproto.Message):
    success: bool = betterproto.bool_field(1)


@dataclass(eq=False, repr=False)
class ModuleBalanceRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class ModuleBalanceResponse(betterproto.Message):
    coins: List["__cosmos_base_v1_beta1__.Coin"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class ModuleLockedAmountRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class ModuleLockedAmountResponse(betterproto.Message):
    coins: List["__cosmos_base_v1_beta1__.Coin"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class AccountUnlockableCoinsRequest(betterproto.Message):
    owner: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class AccountUnlockableCoinsResponse(betterproto.Message):
    coins: List["__cosmos_base_v1_beta1__.Coin"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class AccountUnlockingCoinsRequest(betterproto.Message):
    owner: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class AccountUnlockingCoinsResponse(betterproto.Message):
    coins: List["__cosmos_base_v1_beta1__.Coin"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class AccountLockedCoinsRequest(betterproto.Message):
    owner: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class AccountLockedCoinsResponse(betterproto.Message):
    coins: List["__cosmos_base_v1_beta1__.Coin"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class AccountLockedPastTimeRequest(betterproto.Message):
    owner: str = betterproto.string_field(1)
    timestamp: datetime = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class AccountLockedPastTimeResponse(betterproto.Message):
    locks: List["PeriodLock"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class AccountLockedPastTimeNotUnlockingOnlyRequest(betterproto.Message):
    owner: str = betterproto.string_field(1)
    timestamp: datetime = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class AccountLockedPastTimeNotUnlockingOnlyResponse(betterproto.Message):
    locks: List["PeriodLock"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class AccountUnlockedBeforeTimeRequest(betterproto.Message):
    owner: str = betterproto.string_field(1)
    timestamp: datetime = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class AccountUnlockedBeforeTimeResponse(betterproto.Message):
    locks: List["PeriodLock"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class AccountLockedPastTimeDenomRequest(betterproto.Message):
    owner: str = betterproto.string_field(1)
    timestamp: datetime = betterproto.message_field(2)
    denom: str = betterproto.string_field(3)


@dataclass(eq=False, repr=False)
class AccountLockedPastTimeDenomResponse(betterproto.Message):
    locks: List["PeriodLock"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class LockedDenomRequest(betterproto.Message):
    denom: str = betterproto.string_field(1)
    duration: timedelta = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class LockedDenomResponse(betterproto.Message):
    amount: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class LockedRequest(betterproto.Message):
    lock_id: int = betterproto.uint64_field(1)


@dataclass(eq=False, repr=False)
class LockedResponse(betterproto.Message):
    lock: "PeriodLock" = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class SyntheticLockupsByLockupIdRequest(betterproto.Message):
    lock_id: int = betterproto.uint64_field(1)


@dataclass(eq=False, repr=False)
class SyntheticLockupsByLockupIdResponse(betterproto.Message):
    synthetic_locks: List["SyntheticLock"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class AccountLockedLongerDurationRequest(betterproto.Message):
    owner: str = betterproto.string_field(1)
    duration: timedelta = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class AccountLockedLongerDurationResponse(betterproto.Message):
    locks: List["PeriodLock"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class AccountLockedDurationRequest(betterproto.Message):
    owner: str = betterproto.string_field(1)
    duration: timedelta = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class AccountLockedDurationResponse(betterproto.Message):
    locks: List["PeriodLock"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class AccountLockedLongerDurationNotUnlockingOnlyRequest(betterproto.Message):
    owner: str = betterproto.string_field(1)
    duration: timedelta = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class AccountLockedLongerDurationNotUnlockingOnlyResponse(betterproto.Message):
    locks: List["PeriodLock"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class AccountLockedLongerDurationDenomRequest(betterproto.Message):
    owner: str = betterproto.string_field(1)
    duration: timedelta = betterproto.message_field(2)
    denom: str = betterproto.string_field(3)


@dataclass(eq=False, repr=False)
class AccountLockedLongerDurationDenomResponse(betterproto.Message):
    locks: List["PeriodLock"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class GenesisState(betterproto.Message):
    """GenesisState defines the lockup module's genesis state."""

    last_lock_id: int = betterproto.uint64_field(1)
    locks: List["PeriodLock"] = betterproto.message_field(2)
    synthetic_locks: List["SyntheticLock"] = betterproto.message_field(3)


class MsgStub(betterproto.ServiceStub):
    async def lock_tokens(
        self,
        *,
        owner: str = "",
        duration: timedelta = None,
        coins: Optional[List["__cosmos_base_v1_beta1__.Coin"]] = None
    ) -> "MsgLockTokensResponse":
        coins = coins or []

        request = MsgLockTokens()
        request.owner = owner
        if duration is not None:
            request.duration = duration
        if coins is not None:
            request.coins = coins

        return await self._unary_unary(
            "/osmosis.lockup.Msg/LockTokens", request, MsgLockTokensResponse
        )

    async def begin_unlocking_all(
        self, *, owner: str = ""
    ) -> "MsgBeginUnlockingAllResponse":

        request = MsgBeginUnlockingAll()
        request.owner = owner

        return await self._unary_unary(
            "/osmosis.lockup.Msg/BeginUnlockingAll",
            request,
            MsgBeginUnlockingAllResponse,
        )

    async def begin_unlocking(
        self,
        *,
        owner: str = "",
        id: int = 0,
        coins: Optional[List["__cosmos_base_v1_beta1__.Coin"]] = None
    ) -> "MsgBeginUnlockingResponse":
        coins = coins or []

        request = MsgBeginUnlocking()
        request.owner = owner
        request.id = id
        if coins is not None:
            request.coins = coins

        return await self._unary_unary(
            "/osmosis.lockup.Msg/BeginUnlocking", request, MsgBeginUnlockingResponse
        )

    async def extend_lockup(
        self, *, owner: str = "", id: int = 0, duration: timedelta = None
    ) -> "MsgExtendLockupResponse":

        request = MsgExtendLockup()
        request.owner = owner
        request.id = id
        if duration is not None:
            request.duration = duration

        return await self._unary_unary(
            "/osmosis.lockup.Msg/ExtendLockup", request, MsgExtendLockupResponse
        )


class QueryStub(betterproto.ServiceStub):
    async def module_balance(self) -> "ModuleBalanceResponse":

        request = ModuleBalanceRequest()

        return await self._unary_unary(
            "/osmosis.lockup.Query/ModuleBalance", request, ModuleBalanceResponse
        )

    async def module_locked_amount(self) -> "ModuleLockedAmountResponse":

        request = ModuleLockedAmountRequest()

        return await self._unary_unary(
            "/osmosis.lockup.Query/ModuleLockedAmount",
            request,
            ModuleLockedAmountResponse,
        )

    async def account_unlockable_coins(
        self, *, owner: str = ""
    ) -> "AccountUnlockableCoinsResponse":

        request = AccountUnlockableCoinsRequest()
        request.owner = owner

        return await self._unary_unary(
            "/osmosis.lockup.Query/AccountUnlockableCoins",
            request,
            AccountUnlockableCoinsResponse,
        )

    async def account_unlocking_coins(
        self, *, owner: str = ""
    ) -> "AccountUnlockingCoinsResponse":

        request = AccountUnlockingCoinsRequest()
        request.owner = owner

        return await self._unary_unary(
            "/osmosis.lockup.Query/AccountUnlockingCoins",
            request,
            AccountUnlockingCoinsResponse,
        )

    async def account_locked_coins(
        self, *, owner: str = ""
    ) -> "AccountLockedCoinsResponse":

        request = AccountLockedCoinsRequest()
        request.owner = owner

        return await self._unary_unary(
            "/osmosis.lockup.Query/AccountLockedCoins",
            request,
            AccountLockedCoinsResponse,
        )

    async def account_locked_past_time(
        self, *, owner: str = "", timestamp: datetime = None
    ) -> "AccountLockedPastTimeResponse":

        request = AccountLockedPastTimeRequest()
        request.owner = owner
        if timestamp is not None:
            request.timestamp = timestamp

        return await self._unary_unary(
            "/osmosis.lockup.Query/AccountLockedPastTime",
            request,
            AccountLockedPastTimeResponse,
        )

    async def account_locked_past_time_not_unlocking_only(
        self, *, owner: str = "", timestamp: datetime = None
    ) -> "AccountLockedPastTimeNotUnlockingOnlyResponse":

        request = AccountLockedPastTimeNotUnlockingOnlyRequest()
        request.owner = owner
        if timestamp is not None:
            request.timestamp = timestamp

        return await self._unary_unary(
            "/osmosis.lockup.Query/AccountLockedPastTimeNotUnlockingOnly",
            request,
            AccountLockedPastTimeNotUnlockingOnlyResponse,
        )

    async def account_unlocked_before_time(
        self, *, owner: str = "", timestamp: datetime = None
    ) -> "AccountUnlockedBeforeTimeResponse":

        request = AccountUnlockedBeforeTimeRequest()
        request.owner = owner
        if timestamp is not None:
            request.timestamp = timestamp

        return await self._unary_unary(
            "/osmosis.lockup.Query/AccountUnlockedBeforeTime",
            request,
            AccountUnlockedBeforeTimeResponse,
        )

    async def account_locked_past_time_denom(
        self, *, owner: str = "", timestamp: datetime = None, denom: str = ""
    ) -> "AccountLockedPastTimeDenomResponse":

        request = AccountLockedPastTimeDenomRequest()
        request.owner = owner
        if timestamp is not None:
            request.timestamp = timestamp
        request.denom = denom

        return await self._unary_unary(
            "/osmosis.lockup.Query/AccountLockedPastTimeDenom",
            request,
            AccountLockedPastTimeDenomResponse,
        )

    async def locked_denom(
        self, *, denom: str = "", duration: timedelta = None
    ) -> "LockedDenomResponse":

        request = LockedDenomRequest()
        request.denom = denom
        if duration is not None:
            request.duration = duration

        return await self._unary_unary(
            "/osmosis.lockup.Query/LockedDenom", request, LockedDenomResponse
        )

    async def locked_by_id(self, *, lock_id: int = 0) -> "LockedResponse":

        request = LockedRequest()
        request.lock_id = lock_id

        return await self._unary_unary(
            "/osmosis.lockup.Query/LockedByID", request, LockedResponse
        )

    async def synthetic_lockups_by_lockup_id(
        self,
    ) -> "SyntheticLockupsByLockupIdResponse":

        request = SyntheticLockupsByLockupIdRequest()

        return await self._unary_unary(
            "/osmosis.lockup.Query/SyntheticLockupsByLockupID",
            request,
            SyntheticLockupsByLockupIdResponse,
        )

    async def account_locked_longer_duration(
        self, *, owner: str = "", duration: timedelta = None
    ) -> "AccountLockedLongerDurationResponse":

        request = AccountLockedLongerDurationRequest()
        request.owner = owner
        if duration is not None:
            request.duration = duration

        return await self._unary_unary(
            "/osmosis.lockup.Query/AccountLockedLongerDuration",
            request,
            AccountLockedLongerDurationResponse,
        )

    async def account_locked_duration(
        self, *, owner: str = "", duration: timedelta = None
    ) -> "AccountLockedDurationResponse":

        request = AccountLockedDurationRequest()
        request.owner = owner
        if duration is not None:
            request.duration = duration

        return await self._unary_unary(
            "/osmosis.lockup.Query/AccountLockedDuration",
            request,
            AccountLockedDurationResponse,
        )

    async def account_locked_longer_duration_not_unlocking_only(
        self, *, owner: str = "", duration: timedelta = None
    ) -> "AccountLockedLongerDurationNotUnlockingOnlyResponse":

        request = AccountLockedLongerDurationNotUnlockingOnlyRequest()
        request.owner = owner
        if duration is not None:
            request.duration = duration

        return await self._unary_unary(
            "/osmosis.lockup.Query/AccountLockedLongerDurationNotUnlockingOnly",
            request,
            AccountLockedLongerDurationNotUnlockingOnlyResponse,
        )

    async def account_locked_longer_duration_denom(
        self, *, owner: str = "", duration: timedelta = None, denom: str = ""
    ) -> "AccountLockedLongerDurationDenomResponse":

        request = AccountLockedLongerDurationDenomRequest()
        request.owner = owner
        if duration is not None:
            request.duration = duration
        request.denom = denom

        return await self._unary_unary(
            "/osmosis.lockup.Query/AccountLockedLongerDurationDenom",
            request,
            AccountLockedLongerDurationDenomResponse,
        )


class MsgBase(ServiceBase):
    async def lock_tokens(
        self,
        owner: str,
        duration: timedelta,
        coins: Optional[List["__cosmos_base_v1_beta1__.Coin"]],
    ) -> "MsgLockTokensResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def begin_unlocking_all(self, owner: str) -> "MsgBeginUnlockingAllResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def begin_unlocking(
        self,
        owner: str,
        id: int,
        coins: Optional[List["__cosmos_base_v1_beta1__.Coin"]],
    ) -> "MsgBeginUnlockingResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def extend_lockup(
        self, owner: str, id: int, duration: timedelta
    ) -> "MsgExtendLockupResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_lock_tokens(self, stream: grpclib.server.Stream) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "owner": request.owner,
            "duration": request.duration,
            "coins": request.coins,
        }

        response = await self.lock_tokens(**request_kwargs)
        await stream.send_message(response)

    async def __rpc_begin_unlocking_all(self, stream: grpclib.server.Stream) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "owner": request.owner,
        }

        response = await self.begin_unlocking_all(**request_kwargs)
        await stream.send_message(response)

    async def __rpc_begin_unlocking(self, stream: grpclib.server.Stream) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "owner": request.owner,
            "id": request.id,
            "coins": request.coins,
        }

        response = await self.begin_unlocking(**request_kwargs)
        await stream.send_message(response)

    async def __rpc_extend_lockup(self, stream: grpclib.server.Stream) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "owner": request.owner,
            "id": request.id,
            "duration": request.duration,
        }

        response = await self.extend_lockup(**request_kwargs)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/osmosis.lockup.Msg/LockTokens": grpclib.const.Handler(
                self.__rpc_lock_tokens,
                grpclib.const.Cardinality.UNARY_UNARY,
                MsgLockTokens,
                MsgLockTokensResponse,
            ),
            "/osmosis.lockup.Msg/BeginUnlockingAll": grpclib.const.Handler(
                self.__rpc_begin_unlocking_all,
                grpclib.const.Cardinality.UNARY_UNARY,
                MsgBeginUnlockingAll,
                MsgBeginUnlockingAllResponse,
            ),
            "/osmosis.lockup.Msg/BeginUnlocking": grpclib.const.Handler(
                self.__rpc_begin_unlocking,
                grpclib.const.Cardinality.UNARY_UNARY,
                MsgBeginUnlocking,
                MsgBeginUnlockingResponse,
            ),
            "/osmosis.lockup.Msg/ExtendLockup": grpclib.const.Handler(
                self.__rpc_extend_lockup,
                grpclib.const.Cardinality.UNARY_UNARY,
                MsgExtendLockup,
                MsgExtendLockupResponse,
            ),
        }


class QueryBase(ServiceBase):
    async def module_balance(self) -> "ModuleBalanceResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def module_locked_amount(self) -> "ModuleLockedAmountResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def account_unlockable_coins(
        self, owner: str
    ) -> "AccountUnlockableCoinsResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def account_unlocking_coins(
        self, owner: str
    ) -> "AccountUnlockingCoinsResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def account_locked_coins(self, owner: str) -> "AccountLockedCoinsResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def account_locked_past_time(
        self, owner: str, timestamp: datetime
    ) -> "AccountLockedPastTimeResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def account_locked_past_time_not_unlocking_only(
        self, owner: str, timestamp: datetime
    ) -> "AccountLockedPastTimeNotUnlockingOnlyResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def account_unlocked_before_time(
        self, owner: str, timestamp: datetime
    ) -> "AccountUnlockedBeforeTimeResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def account_locked_past_time_denom(
        self, owner: str, timestamp: datetime, denom: str
    ) -> "AccountLockedPastTimeDenomResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def locked_denom(
        self, denom: str, duration: timedelta
    ) -> "LockedDenomResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def locked_by_id(self, lock_id: int) -> "LockedResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def synthetic_lockups_by_lockup_id(
        self,
    ) -> "SyntheticLockupsByLockupIdResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def account_locked_longer_duration(
        self, owner: str, duration: timedelta
    ) -> "AccountLockedLongerDurationResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def account_locked_duration(
        self, owner: str, duration: timedelta
    ) -> "AccountLockedDurationResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def account_locked_longer_duration_not_unlocking_only(
        self, owner: str, duration: timedelta
    ) -> "AccountLockedLongerDurationNotUnlockingOnlyResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def account_locked_longer_duration_denom(
        self, owner: str, duration: timedelta, denom: str
    ) -> "AccountLockedLongerDurationDenomResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_module_balance(self, stream: grpclib.server.Stream) -> None:
        request = await stream.recv_message()

        request_kwargs = {}

        response = await self.module_balance(**request_kwargs)
        await stream.send_message(response)

    async def __rpc_module_locked_amount(self, stream: grpclib.server.Stream) -> None:
        request = await stream.recv_message()

        request_kwargs = {}

        response = await self.module_locked_amount(**request_kwargs)
        await stream.send_message(response)

    async def __rpc_account_unlockable_coins(
        self, stream: grpclib.server.Stream
    ) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "owner": request.owner,
        }

        response = await self.account_unlockable_coins(**request_kwargs)
        await stream.send_message(response)

    async def __rpc_account_unlocking_coins(
        self, stream: grpclib.server.Stream
    ) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "owner": request.owner,
        }

        response = await self.account_unlocking_coins(**request_kwargs)
        await stream.send_message(response)

    async def __rpc_account_locked_coins(self, stream: grpclib.server.Stream) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "owner": request.owner,
        }

        response = await self.account_locked_coins(**request_kwargs)
        await stream.send_message(response)

    async def __rpc_account_locked_past_time(
        self, stream: grpclib.server.Stream
    ) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "owner": request.owner,
            "timestamp": request.timestamp,
        }

        response = await self.account_locked_past_time(**request_kwargs)
        await stream.send_message(response)

    async def __rpc_account_locked_past_time_not_unlocking_only(
        self, stream: grpclib.server.Stream
    ) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "owner": request.owner,
            "timestamp": request.timestamp,
        }

        response = await self.account_locked_past_time_not_unlocking_only(
            **request_kwargs
        )
        await stream.send_message(response)

    async def __rpc_account_unlocked_before_time(
        self, stream: grpclib.server.Stream
    ) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "owner": request.owner,
            "timestamp": request.timestamp,
        }

        response = await self.account_unlocked_before_time(**request_kwargs)
        await stream.send_message(response)

    async def __rpc_account_locked_past_time_denom(
        self, stream: grpclib.server.Stream
    ) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "owner": request.owner,
            "timestamp": request.timestamp,
            "denom": request.denom,
        }

        response = await self.account_locked_past_time_denom(**request_kwargs)
        await stream.send_message(response)

    async def __rpc_locked_denom(self, stream: grpclib.server.Stream) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "denom": request.denom,
            "duration": request.duration,
        }

        response = await self.locked_denom(**request_kwargs)
        await stream.send_message(response)

    async def __rpc_locked_by_id(self, stream: grpclib.server.Stream) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "lock_id": request.lock_id,
        }

        response = await self.locked_by_id(**request_kwargs)
        await stream.send_message(response)

    async def __rpc_synthetic_lockups_by_lockup_id(
        self, stream: grpclib.server.Stream
    ) -> None:
        request = await stream.recv_message()

        request_kwargs = {}

        response = await self.synthetic_lockups_by_lockup_id(**request_kwargs)
        await stream.send_message(response)

    async def __rpc_account_locked_longer_duration(
        self, stream: grpclib.server.Stream
    ) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "owner": request.owner,
            "duration": request.duration,
        }

        response = await self.account_locked_longer_duration(**request_kwargs)
        await stream.send_message(response)

    async def __rpc_account_locked_duration(
        self, stream: grpclib.server.Stream
    ) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "owner": request.owner,
            "duration": request.duration,
        }

        response = await self.account_locked_duration(**request_kwargs)
        await stream.send_message(response)

    async def __rpc_account_locked_longer_duration_not_unlocking_only(
        self, stream: grpclib.server.Stream
    ) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "owner": request.owner,
            "duration": request.duration,
        }

        response = await self.account_locked_longer_duration_not_unlocking_only(
            **request_kwargs
        )
        await stream.send_message(response)

    async def __rpc_account_locked_longer_duration_denom(
        self, stream: grpclib.server.Stream
    ) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "owner": request.owner,
            "duration": request.duration,
            "denom": request.denom,
        }

        response = await self.account_locked_longer_duration_denom(**request_kwargs)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/osmosis.lockup.Query/ModuleBalance": grpclib.const.Handler(
                self.__rpc_module_balance,
                grpclib.const.Cardinality.UNARY_UNARY,
                ModuleBalanceRequest,
                ModuleBalanceResponse,
            ),
            "/osmosis.lockup.Query/ModuleLockedAmount": grpclib.const.Handler(
                self.__rpc_module_locked_amount,
                grpclib.const.Cardinality.UNARY_UNARY,
                ModuleLockedAmountRequest,
                ModuleLockedAmountResponse,
            ),
            "/osmosis.lockup.Query/AccountUnlockableCoins": grpclib.const.Handler(
                self.__rpc_account_unlockable_coins,
                grpclib.const.Cardinality.UNARY_UNARY,
                AccountUnlockableCoinsRequest,
                AccountUnlockableCoinsResponse,
            ),
            "/osmosis.lockup.Query/AccountUnlockingCoins": grpclib.const.Handler(
                self.__rpc_account_unlocking_coins,
                grpclib.const.Cardinality.UNARY_UNARY,
                AccountUnlockingCoinsRequest,
                AccountUnlockingCoinsResponse,
            ),
            "/osmosis.lockup.Query/AccountLockedCoins": grpclib.const.Handler(
                self.__rpc_account_locked_coins,
                grpclib.const.Cardinality.UNARY_UNARY,
                AccountLockedCoinsRequest,
                AccountLockedCoinsResponse,
            ),
            "/osmosis.lockup.Query/AccountLockedPastTime": grpclib.const.Handler(
                self.__rpc_account_locked_past_time,
                grpclib.const.Cardinality.UNARY_UNARY,
                AccountLockedPastTimeRequest,
                AccountLockedPastTimeResponse,
            ),
            "/osmosis.lockup.Query/AccountLockedPastTimeNotUnlockingOnly": grpclib.const.Handler(
                self.__rpc_account_locked_past_time_not_unlocking_only,
                grpclib.const.Cardinality.UNARY_UNARY,
                AccountLockedPastTimeNotUnlockingOnlyRequest,
                AccountLockedPastTimeNotUnlockingOnlyResponse,
            ),
            "/osmosis.lockup.Query/AccountUnlockedBeforeTime": grpclib.const.Handler(
                self.__rpc_account_unlocked_before_time,
                grpclib.const.Cardinality.UNARY_UNARY,
                AccountUnlockedBeforeTimeRequest,
                AccountUnlockedBeforeTimeResponse,
            ),
            "/osmosis.lockup.Query/AccountLockedPastTimeDenom": grpclib.const.Handler(
                self.__rpc_account_locked_past_time_denom,
                grpclib.const.Cardinality.UNARY_UNARY,
                AccountLockedPastTimeDenomRequest,
                AccountLockedPastTimeDenomResponse,
            ),
            "/osmosis.lockup.Query/LockedDenom": grpclib.const.Handler(
                self.__rpc_locked_denom,
                grpclib.const.Cardinality.UNARY_UNARY,
                LockedDenomRequest,
                LockedDenomResponse,
            ),
            "/osmosis.lockup.Query/LockedByID": grpclib.const.Handler(
                self.__rpc_locked_by_id,
                grpclib.const.Cardinality.UNARY_UNARY,
                LockedRequest,
                LockedResponse,
            ),
            "/osmosis.lockup.Query/SyntheticLockupsByLockupID": grpclib.const.Handler(
                self.__rpc_synthetic_lockups_by_lockup_id,
                grpclib.const.Cardinality.UNARY_UNARY,
                SyntheticLockupsByLockupIdRequest,
                SyntheticLockupsByLockupIdResponse,
            ),
            "/osmosis.lockup.Query/AccountLockedLongerDuration": grpclib.const.Handler(
                self.__rpc_account_locked_longer_duration,
                grpclib.const.Cardinality.UNARY_UNARY,
                AccountLockedLongerDurationRequest,
                AccountLockedLongerDurationResponse,
            ),
            "/osmosis.lockup.Query/AccountLockedDuration": grpclib.const.Handler(
                self.__rpc_account_locked_duration,
                grpclib.const.Cardinality.UNARY_UNARY,
                AccountLockedDurationRequest,
                AccountLockedDurationResponse,
            ),
            "/osmosis.lockup.Query/AccountLockedLongerDurationNotUnlockingOnly": grpclib.const.Handler(
                self.__rpc_account_locked_longer_duration_not_unlocking_only,
                grpclib.const.Cardinality.UNARY_UNARY,
                AccountLockedLongerDurationNotUnlockingOnlyRequest,
                AccountLockedLongerDurationNotUnlockingOnlyResponse,
            ),
            "/osmosis.lockup.Query/AccountLockedLongerDurationDenom": grpclib.const.Handler(
                self.__rpc_account_locked_longer_duration_denom,
                grpclib.const.Cardinality.UNARY_UNARY,
                AccountLockedLongerDurationDenomRequest,
                AccountLockedLongerDurationDenomResponse,
            ),
        }


from ...cosmos.base import v1beta1 as __cosmos_base_v1_beta1__
