from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="market-index"),
    path('trade', views.trade, name="market-trade"),
    path('order', views.order, name="market-order"),
    path('trade-report', views.trade_report, name="trade-report"),
    path('order-report', views.order_report, name="order-report"),
]
