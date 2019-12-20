# -*- coding: utf-8 -*-
import json
from datetime import datetime
from decimal import Decimal

import scrapy
from django.utils import timezone
from scrapy import Request

from crawler.items import TickItem
from exchange.models import Symbol


class TicksSpider(scrapy.Spider):
    name = 'ticks'

    def start_requests(self):

        from exchange.exchange_platform.huobi import Huobi

        exchanges = [Huobi]
        symbols = ["BTC_USDT"]

        for exchange in exchanges:
            ex = exchange()
            ex.set_exchange_orm_obj()

            for symbol in symbols:
                ticks_url = ex.build_ticks_url(symbol)

                base, quote = symbol.split("_")

                yield Request(
                    ticks_url,
                    meta={
                        "exchange_orm_obj": ex.exchange_orm_obj,
                        "symbol": Symbol.objects.get(base__name__iexact=base, quote__name__iexact=quote)
                    }
                )

    def parse(self, response):
        resp = json.loads(response.body_as_unicode())

        for d in resp["data"]:
            for tick in d["data"]:

                item = TickItem()

                _price = Decimal(tick["price"])
                _amount = Decimal(tick["amount"])

                item["exchange"] = response.meta["exchange_orm_obj"]
                item["symbol"] = response.meta["symbol"]
                item["trade_time"] = self.ts_to_dt(tick["ts"] / 1000)
                item["price"] = _price
                item["amount"] = _amount
                item["value"] = _price * _amount

                yield item

    @staticmethod
    def ts_to_dt(ts):
        tz = timezone.get_default_timezone()

        dt = datetime.fromtimestamp(ts)
        dt = timezone.make_aware(dt, tz)
        return dt
