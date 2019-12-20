from django.db import models

from exchange.models import Exchange, Symbol


class Tick(models.Model):
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)

    trade_time = models.DateTimeField(blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=10)
    amount = models.DecimalField(max_digits=20, decimal_places=10)

    # value = price * amount
    value = models.DecimalField(max_digits=20, decimal_places=10)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("exchange", "symbol", "amount", "price", "trade_time")

    def __str__(self):
        return f"<Tick of {self.symbol} @ {self.exchange}>"
