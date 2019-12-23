from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="market-index"),
    path('analyze', views.analyze, name="market-analyze"),
]
