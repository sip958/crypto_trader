from django.db import models

from enums.market import OrderSideEnum
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


class Order(models.Model):
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)

    sequence = models.CharField(max_length=256, unique=True)
    order_id = models.CharField(max_length=256)
    side = models.CharField(
        max_length=128,
        choices=((s.name, s.value) for s in OrderSideEnum)
    )
    time = models.DateTimeField()
    price = models.DecimalField(max_digits=40, decimal_places=20)
    amount = models.DecimalField(max_digits=40, decimal_places=20)

    value = models.DecimalField(max_digits=40, decimal_places=20)

    def __str__(self):
        return f"<Order: {self.sequence}>"
