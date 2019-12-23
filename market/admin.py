from django.contrib import admin

from market.models import Tick, Order


@admin.register(Tick)
class TickAdmin(admin.ModelAdmin):
    list_display = ("__str__", "exchange", "symbol", "price", "amount", "value", "trade_time", "created",)
    list_editable = ("exchange", "symbol", "price", "amount", "value",)

    list_filter = (
        ("exchange", admin.RelatedOnlyFieldListFilter),
        ("symbol", admin.RelatedOnlyFieldListFilter),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("__str__", "exchange", "sequence", "symbol", "price", "amount", "side", "value", "time",)
    # list_editable = ("exchange", "symbol", "price", "amount", "value",)

    list_filter = (
        ("exchange", admin.RelatedOnlyFieldListFilter),
        ("symbol", admin.RelatedOnlyFieldListFilter),
    )

