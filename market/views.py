import base64

import seaborn as sns
import pandas as pd
import numpy as np

from io import BytesIO
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render
from django.template.loader import render_to_string
from matplotlib import pyplot as plt

from exchange.models import Exchange, Symbol
from market.models import Tick, Order


pd.options.display.float_format = '{:.6f}'.format
sns.set(style="darkgrid")


def index(request):
    return render(request, "market/index.html", {
        "symbols": Symbol.objects.all(),
        "exchanges": Exchange.objects.all(),
    })


def trade(request):
    return render(request, "market/trade.html", {
        "symbols": Symbol.objects.all(),
        "exchanges": Exchange.objects.all(),
    })


def order(request):
    return render(request, "market/order.html", {
        "symbols": Symbol.objects.all(),
        "exchanges": Exchange.objects.filter(name__iexact="KuCoin"),
    })


def order_report(request):
    base = request.POST.get("base")
    quote = request.POST.get("quote")
    exchange = "KuCoin"  # only KuCoin provides dataset of orders

    value_lower_bound = float(request.POST.get("value_lower_bound"))
    value_upper_bound = float(request.POST.get("value_upper_bound"))
    value_nbins = int(request.POST.get("value_nbins"))

    quantity_lower_bound = float(request.POST.get("quantity_lower_bound"))
    quantity_upper_bound = float(request.POST.get("quantity_upper_bound"))
    quantity_nbins = int(request.POST.get("quantity_nbins"))

    symbol = Symbol.objects.get(base__name__iexact=base, quote__name__iexact=quote)
    exchange = Exchange.objects.get(name__iexact=exchange)

    df = pd.DataFrame(
        list(Order.objects.filter(exchange=exchange, symbol=symbol).values("price", "amount", "time"))
    )

    df["price"] = pd.to_numeric(df["price"])
    df["quantity"] = pd.to_numeric(df["amount"])

    del df["amount"]

    df["value"] = df["price"] * df["quantity"]
    df.set_index("time", inplace=True)

    value_size = df.loc[(df["value"] >= value_lower_bound) & (df["value"] <= value_upper_bound)]["value"]
    value_bins = pd.Series(np.linspace(value_lower_bound, value_upper_bound, value_nbins + 1))
    value_out = pd.cut(value_size, value_bins)
    value_out_norm = value_out.value_counts(sort=False)
    value_x = value_out_norm.index
    value_y = value_out_norm

    plt.xticks(rotation=90, fontsize=6)
    sns.barplot(x=value_x, y=value_y)
    plt.xlabel("Value Range of Orders")
    plt.ylabel("Count")
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=settings.PLOT_DPI)
    value_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    plt.show(block=False)

    quantity_size = df.loc[(df["quantity"] >= quantity_lower_bound) & (df["quantity"] <= quantity_upper_bound)]["quantity"]
    quantity_bins = pd.Series(np.linspace(quantity_lower_bound, quantity_upper_bound, quantity_nbins + 1))
    quantity_out = pd.cut(quantity_size, quantity_bins)
    quantity_out_norm = quantity_out.value_counts(sort=False)
    quantity_x = quantity_out_norm.index
    quantity_y = quantity_out_norm

    plt.xticks(rotation=90, fontsize=6)
    sns.barplot(x=quantity_x, y=quantity_y)
    plt.xlabel("Quantity Range of Orders")
    plt.ylabel("Count")
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=settings.PLOT_DPI)
    quantity_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    plt.show(block=False)

    return JsonResponse({
        "html": render_to_string("market/order_report.html", {
            "order_num": len(df),

            "value_src": f"data:image/png;base64,{value_data}",
            "quantity_src": f"data:image/png;base64,{quantity_data}",

            "symbol": symbol,
            "exchange": exchange,
            "describe": df.describe().to_html(classes="table is-bordered is-striped is-hoverable is-fullwidth".split()),

        })
    })


def trade_report(request):
    base = request.POST.get("base")
    quote = request.POST.get("quote")
    exchange = request.POST.get("exchange")

    value_lower_bound = float(request.POST.get("value_lower_bound"))
    value_upper_bound = float(request.POST.get("value_upper_bound"))
    value_nbins = int(request.POST.get("value_nbins"))

    quantity_lower_bound = float(request.POST.get("quantity_lower_bound"))
    quantity_upper_bound = float(request.POST.get("quantity_upper_bound"))
    quantity_nbins = int(request.POST.get("quantity_nbins"))

    symbol = Symbol.objects.get(base__name__iexact=base, quote__name__iexact=quote)
    exchange = Exchange.objects.get(name__iexact=exchange)

    df = pd.DataFrame(
        list(Tick.objects.filter(exchange=exchange, symbol=symbol).values("price", "amount", "trade_time"))
    )

    df["price"] = pd.to_numeric(df["price"])
    df["quantity"] = pd.to_numeric(df["amount"])

    del df["amount"]

    df["value"] = df["price"] * df["quantity"]
    df.set_index("trade_time", inplace=True)

    value_size = df.loc[(df["value"] >= value_lower_bound) & (df["value"] <= value_upper_bound)]["value"]
    value_bins = pd.Series(np.linspace(value_lower_bound, value_upper_bound, value_nbins + 1))
    value_out = pd.cut(value_size, value_bins)
    value_out_norm = value_out.value_counts(sort=False)
    value_x = value_out_norm.index
    value_y = value_out_norm

    plt.xticks(rotation=90, fontsize=6)
    sns.barplot(x=value_x, y=value_y)
    plt.xlabel("Value Range of Orders")
    plt.ylabel("Count")
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=settings.PLOT_DPI)
    value_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    plt.show(block=False)

    quantity_size = df.loc[(df["quantity"] >= quantity_lower_bound) & (df["quantity"] <= quantity_upper_bound)][
        "quantity"]
    quantity_bins = pd.Series(np.linspace(quantity_lower_bound, quantity_upper_bound, quantity_nbins + 1))
    quantity_out = pd.cut(quantity_size, quantity_bins)
    quantity_out_norm = quantity_out.value_counts(sort=False)
    quantity_x = quantity_out_norm.index
    quantity_y = quantity_out_norm

    plt.xticks(rotation=90, fontsize=6)
    sns.barplot(x=quantity_x, y=quantity_y)
    plt.xlabel("Quantity Range of Orders")
    plt.ylabel("Count")
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=settings.PLOT_DPI)
    quantity_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    plt.show(block=False)

    return JsonResponse({
        "html": render_to_string("market/trade_report.html", {
            "trade_num": len(df),

            "value_src": f"data:image/png;base64,{value_data}",
            "quantity_src": f"data:image/png;base64,{quantity_data}",

            "symbol": symbol,
            "exchange": exchange,
            "describe": df.describe().to_html(classes="table is-bordered is-striped is-hoverable is-fullwidth".split()),

        })
    })
