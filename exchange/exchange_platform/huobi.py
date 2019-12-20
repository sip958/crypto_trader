from ._base import BasePlatform


class Huobi(BasePlatform):
    def build_ticks_url(self, symbol_str, *args, **kwargs):
        symbol_str = self.build_symbol_str(symbol_str)
        ticks_url = f"https://api.huobi.pro/market/history/trade?symbol={symbol_str}&size=2000"
        return ticks_url

    async def format_ticks(self, *args, **kwargs):
        pass
