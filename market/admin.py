from django.contrib import admin
from django.conf.locale.en import formats as en_formats

from market.models import Tick, Order

en_formats.DATETIME_FORMAT = 'Y-m-d H:i:s.u'


@admin.register(Tick)
class TickAdmin(admin.ModelAdmin):
    list_display = ("__str__", "exchange", "symbol", "price", "amount", "value", "trade_time", "created",)
    list_editable = ("exchange", "symbol", "price", "amount", "value",)

    list_filter = (
        ("exchange", admin.RelatedOnlyFieldListFilter),
        ("symbol", admin.RelatedFieldListFilter),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("__str__", "exchange", "sequence", "symbol", "price", "amount", "side", "value", "time",)
    # list_editable = ("exchange", "symbol", "price", "amount", "value",)

    list_filter = (
        ("exchange", admin.RelatedOnlyFieldListFilter),
        ("symbol", admin.RelatedFieldListFilter),
    )
