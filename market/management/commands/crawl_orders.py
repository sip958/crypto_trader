"""
KuCoin Only
"""
import asyncio
import logging
import os
from decimal import Decimal

from django.core.management import BaseCommand
from django.utils.module_loading import import_string

from common.utils import ts_to_dt
from enums.market import OrderSideEnum
from exchange.models import Exchange, Symbol
from market.models import Order

logger = logging.getLogger("django")


async def main(observable, symbol, exchange):
    class WebsocketObserver(object):

        def __init__(self):
            self.orm_cache = []

        async def on_order(self, order):

            print(f"on_order: {order}")

            if order["type"] in ["received", "match", "done", "change"]:
                return

            _price = Decimal(order["price"])
            _amount = Decimal(order["size"])

            self.orm_cache.append(Order(
                exchange=exchange,
                symbol=symbol,
                sequence=order["sequence"],
                order_id=order["orderId"],
                side=OrderSideEnum.SELL.name if order["side"] == "sell" else OrderSideEnum.BUY.name,
                time=ts_to_dt(int(order["time"]) / 10 ** 9),
                price=_price,
                amount=_amount,
                value=_price * _amount,
            ))

            if len(self.orm_cache) >= 50:
                Order.objects.bulk_create(self.orm_cache, ignore_conflicts=True)

                self.orm_cache = []

    count_before_fetch = Order.objects.filter(exchange=exchange, symbol=symbol).count()

    observable.attach_observer(WebsocketObserver())
    await observable.connect()
    asyncio.ensure_future(observable.start_fetch_order_book())  # just let it run in the io loop

    count_after_fetch = Order.objects.filter(exchange=exchange, symbol=symbol).count()

    logger.info(
        f"after fetch, the number of trade ({symbol} @ {exchange}): {count_before_fetch} ==> {count_after_fetch}"
    )


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--base', required=True, type=str)
        parser.add_argument('--quote', required=True, type=str)
        # parser.add_argument('--ex', required=True, type=str)

    def handle(self, *args, **options):
        str_base = options["base"].upper()
        str_quote = options["quote"].upper()
        # str_ex = options["ex"]
        str_ex = "kucoin"

        try:
            symbol = Symbol.objects.get(
                base__name__iexact=str_base,
                quote__name__iexact=str_quote,
            )
            ex = Exchange.objects.get(name__iexact=str_ex)

        except Symbol.DoesNotExist:
            self.stdout.write(self.style.ERROR("Symbol Does Not Exist. ({}/{})".format(str_base, str_quote)))
            if_create = input("Create? [y/N]")

            if if_create == "y":
                self.stdout.write(self.style.NOTICE("Creating..."))

                symbol = Symbol.objects.create(
                    base=str_base,
                    quote=str_quote,
                )

                self.stdout.write(self.style.NOTICE("Created Symbol [{}]".format(symbol)))
        except Exchange.DoesNotExist:
            self.stdout.write(self.style.ERROR("Exchange Does Not Exist. ({})".format(str_ex)))
        else:
            self.stdout.write(self.style.NOTICE(f"Starting collecting orders of [{symbol} ON {ex}]"))

            from exchange.websocket_observable.kucoin import KuCoinWebsocketObservable

            ws_observable_path = f"exchange.websocket_observable.{ex.name.lower()}.{ex.name}WebsocketObservable"

            ws_observable_class = import_string(ws_observable_path)

            ws_observable = ws_observable_class()
            ws_observable.set_symbol("BTC-USDT")

            loop = asyncio.get_event_loop()

            loop.run_until_complete(main(ws_observable, symbol, ex))

            self.stdout.write(self.style.NOTICE(f"Press Ctrl+{'Break' if os.name == 'nt' else 'C'} to exit"))

            try:
                loop.run_forever()
            except (KeyboardInterrupt, SystemExit):
                self.stdout.write(self.style.NOTICE("Program Terminating..."))
