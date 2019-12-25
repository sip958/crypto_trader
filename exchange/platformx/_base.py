from typing import Optional

from common.utils import symbol_format_convert
from enums.symbol import SymbolFormatEnum
from exchange.models import Exchange
from exchange.websocket_observable._base import BaseWsObservable


class BasePlatform(object):

    def __init__(self):
        self.exchange_orm_obj = None
        self.trade_engine = None
        self.websocket_observable = None

    def set_exchange_orm_obj(self, obj: Optional[Exchange] = None) -> None:
        if obj is None:
            obj = Exchange.objects.get(name__iexact=self.__class__.__name__)
        # self.exchange_controller.orm_obj = obj
        # ExchangeService.getTicks(self.orm_obj)
        # self.exchange_controller.getTicks()
        self.exchange_orm_obj = obj

    def set_websocket_observable(self, observable: BaseWsObservable) -> None:
        self.websocket_observable = observable

    def build_symbol_str(self, symbol_str):
        to_format = getattr(SymbolFormatEnum, self.exchange_orm_obj.symbol_format)

        symbol_str = symbol_format_convert(
            symbol_str,
            from_format=SymbolFormatEnum.UPPER_UNDERSCORE,
            to_format=to_format
        )
        return symbol_str

    def format_ticks(self, *args, **kwargs):
        raise NotImplementedError

    def build_ticks_url(self, *args, **kwargs):
        raise NotImplementedError

    def fetch_ticks(self, symbol, *args, **kwargs):
        pass

    def __str__(self):
        return f"{self.__class__.__name__}"
