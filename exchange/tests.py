from django.test import TestCase

from enums.symbol import SymbolFormatEnum
from exchange.exchange_platform.huobi import Huobi
from exchange.models import Exchange


class PlatformTest(TestCase):

    def setUp(self):
        Exchange.objects.create(name="Huobi", symbol_format=SymbolFormatEnum.LOWER.name)

        huobi_orm_obj = Exchange.objects.get(name__iexact="huobi")

        self.huobi = Huobi()
        self.huobi.set_exchange_orm_obj(huobi_orm_obj)

    def test_symbol_str(self):
        SYMBOL_STRING = "BTC_USDT"

        huobi_symbol_str = self.huobi.build_symbol_str(SYMBOL_STRING)

        self.assertEqual(huobi_symbol_str, "btcusdt")

    def test_ticks_url(self):
        SYMBOL_STRING = "BTC_USDT"

        huobi_ticks_url = self.huobi.build_ticks_url(SYMBOL_STRING)

        print(huobi_ticks_url)

        self.assertIsInstance(huobi_ticks_url, str)
