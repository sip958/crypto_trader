from django.contrib import admin

from market.models import Tick


@admin.register(Tick)
class TickAdmin(admin.ModelAdmin):
    list_display = ("__str__", "exchange", "symbol", "price", "amount", "value", "trade_time", "created",)
    list_editable = ("exchange", "symbol", "price", "amount", "value",)

    list_filter = (
        ("exchange", admin.RelatedOnlyFieldListFilter),
        ("symbol", admin.RelatedOnlyFieldListFilter),
    )

