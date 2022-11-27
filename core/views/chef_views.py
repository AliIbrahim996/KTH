from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Chef
from core.serializer import ChefListSerializer


class ChefView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ChefListSerializer

    def get(self, request, *args, **kwargs):
        chefs = Chef.objects.all()

        serializer = self.serializer_class(chefs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class BestChefsView(ChefView):

    def get(self, request, *args, **kwargs):
        chefs = Chef.objects.filter().order_by("-heart_number")

        serializer = self.serializer_class(chefs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
