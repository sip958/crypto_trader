import base64
from io import BytesIO

import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from matplotlib import pyplot as plt

from exchange.models import Exchange, Symbol
from market.models import Tick

plt.style.use('seaborn-poster')


def index(request):
    return render(request, "market/index.html", {
        "symbols": Symbol.objects.all(),
        "exchanges": Exchange.objects.all(),
    })


def analyze(request):
    base = request.POST.get("base")
    quote = request.POST.get("quote")
    exchange = request.POST.get("exchange")

    symbol = Symbol.objects.get(base__name__iexact=base, quote__name__iexact=quote)
    exchange = Exchange.objects.get(name__iexact=exchange)

    df = pd.DataFrame(
        list(Tick.objects.filter(exchange=exchange, symbol=symbol).values("price", "amount", "trade_time"))
    )

    df["price"] = pd.to_numeric(df["price"])
    df["amount"] = pd.to_numeric(df["amount"])
    df["quantity"] = pd.to_numeric(df["amount"])

    df["value"] = df["price"] * df["amount"]
    df.set_index("trade_time", inplace=True)

    value_range = (0, 100)
    quantity_range = (0, 2)

    value = df.value

    plt.hist(value)
    buf = BytesIO()
    plt.savefig(buf, format="png")
    value_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    plt.show(block=False)

    plt.hist(value, bins=22, range=value_range)
    buf = BytesIO()
    plt.savefig(buf, format="png")
    value_scaled_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    plt.show(block=False)

    ax1 = plt.subplot("211")
    ax2 = plt.subplot("212")
    ax1.hist(value, bins=22)
    ax2.hist(value, bins=22, range=value_range)
    buf = BytesIO()
    plt.savefig(buf, format="png")
    value_together_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    plt.show(block=False)

    quantity = df.quantity
    plt.hist(quantity)
    buf = BytesIO()
    plt.savefig(buf, format="png")
    quantity_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    plt.show(block=False)

    plt.hist(quantity, bins=22, range=quantity_range)
    buf = BytesIO()
    plt.savefig(buf, format="png")
    quantity_scaled_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    plt.show(block=False)

    ax1 = plt.subplot("211")
    ax2 = plt.subplot("212")
    ax1.hist(quantity, bins=22)
    ax2.hist(quantity, bins=22, range=quantity_range)
    buf = BytesIO()
    plt.savefig(buf, format="png")
    quantity_together_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    plt.show(block=False)

    return JsonResponse({
        "html": render_to_string("market/analyze_response.html", {
            "order_num": (10 ** 5) + 12,
            "trade_num": len(df),
            "value_src": f"data:image/png;base64,{value_data}",
            "value_src_scaled": f"data:image/png;base64,{value_scaled_data}",
            "value_src_together": f"data:image/png;base64,{value_together_data}",

            "quantity_src": f"data:image/png;base64,{quantity_data}",
            "quantity_src_scaled": f"data:image/png;base64,{quantity_scaled_data}",
            "quantity_src_together": f"data:image/png;base64,{quantity_together_data}",

            "symbol": symbol,
            "exchange": exchange,
            "head": df.head().to_html(classes="table is-bordered is-striped is-hoverable is-fullwidth".split()),
            "describe": df.describe().to_html(classes="table is-bordered is-striped is-hoverable is-fullwidth".split()),

        })
    })
