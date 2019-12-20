from django.db import models

from enums.symbol import SymbolFormatEnum


class Currency(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return "{}".format(self.name)


class Exchange(models.Model):
    name = models.CharField(max_length=2048)
    description = models.CharField(max_length=10 ** 5, blank=True)
    url = models.URLField(blank=True)

    symbol_format = models.CharField(
        max_length=128,
        choices=[(format.name, format) for format in SymbolFormatEnum],
        default=SymbolFormatEnum.UPPER_UNDERSCORE.name
    )

    def __str__(self):
        return f"<Exchange: {self.name}>"


class Symbol(models.Model):
    base = models.ForeignKey(to="Currency", related_name="symbol_base", on_delete=models.CASCADE)
    quote = models.ForeignKey(to="Currency", related_name="symbol_quote", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("base", "quote")

    def __str__(self):
        return f"<Symbol: {self.base}_{self.quote}>"


def symbol_str_2_orm(symbol_str: str) -> Symbol:
    base, quote = symbol_str.split("_")
    return Symbol.objects.get(base__name__iexact=base, quote__name__iexact=quote)
