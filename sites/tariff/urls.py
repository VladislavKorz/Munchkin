from django.urls import path
from .views import *

urlpatterns = [
    path('get_tariff/', TariffListView.as_view(), name='tariff-list'),
    path('get_cost/<int:users>/', TariffCostView.as_view(), name='tariff-cost')
]
