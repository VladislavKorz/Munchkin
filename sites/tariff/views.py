from rest_framework import generics
from .models import Tariff
from .serializers import TariffSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



class TariffListView(generics.ListAPIView):
    queryset = Tariff.objects.all()
    serializer_class = TariffSerializer


class TariffCostView(APIView):
    def get(self, request, users, format=None):
        try:
            # Найдем тариф с минимальной ценой
            tariff = Tariff.objects.order_by('price').first()
            # Умножим количество пользователей на цену тарифа
            total_cost = (users * tariff.price) - (users * tariff.price * 0.077)

            return Response({'total_cost': total_cost}, status=status.HTTP_200_OK)
        except Tariff.DoesNotExist:
            return Response({'message': 'Тарифы не найдены'}, status=status.HTTP_404_NOT_FOUND)
