# -*- coding: utf-8 -*-
import json

import scrapy
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
                        "exchange": ex,
                        "symbol": Symbol.objects.get(base__name__iexact=base, quote__name__iexact=quote)
                    }
                )

    def parse(self, response):
        resp = json.loads(response.body_as_unicode())

        exchange = response.meta["exchange"]
        symbol = response.meta["symbol"]

        ticks = exchange.format_ticks(resp, symbol=symbol)

        for tick in ticks:
            item = TickItem()
            item["exchange"] = tick.exchange
            item["symbol"] = tick.symbol
            item["trade_time"] = tick.trade_time
            item["price"] = tick.price
            item["amount"] = tick.amount
            item["value"] = tick.value

            yield item
