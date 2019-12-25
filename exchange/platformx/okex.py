from decimal import Decimal
from typing import Union, Sequence

from common.utils import dt_str_to_dt
from exchange.models import Symbol, symbol_str_2_orm
from market.models import Tick
from ._base import BasePlatform


class OkEx(BasePlatform):
    def build_ticks_url(self, symbol_str, *args, **kwargs):
        symbol_str = self.build_symbol_str(symbol_str)
        ticks_url = f"https://www.okex.com/api/spot/v3/instruments/{symbol_str}/trades?limit=2000"
        return ticks_url

    def format_ticks(self, response, *args, symbol: Union[str, Symbol, None] = None, **kwargs) -> Sequence[Tick]:

        if not symbol:
            raise ValueError("Missing Argument: `symbol`")

        symbol = symbol_str_2_orm(symbol) if isinstance(symbol, str) else symbol

        ticks = []
        for tick in response:
            _price = Decimal(tick["price"])
            _amount = Decimal(tick["size"])

            ticks.append(Tick(
                exchange=self.exchange_orm_obj,
                symbol=symbol,
                trade_time=dt_str_to_dt(tick["timestamp"]),
                price=_price,
                amount=_amount,
                value=_price * _amount
            ))
        return ticks
