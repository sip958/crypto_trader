from django.contrib import admin

from .models import Exchange, Symbol, Currency


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("__str__", "name",)
    list_editable = ("name",)


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ("__str__", "name", "description", "url", "symbol_format")
    list_editable = ("name", "description", "url", "symbol_format")


@admin.register(Symbol)
class SymbolAdmin(admin.ModelAdmin):
    list_display = ("__str__", "base", "quote",)
    list_editable = ("base", "quote",)
