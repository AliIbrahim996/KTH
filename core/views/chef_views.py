from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Chef
from core.serializer import ChefListSerilizer, ChefRegistrationSerializer

class bestChefsView(APIView):
    serializer_class = ChefRegistrationSerializer

    def get(self, request, *args, **kwargs):

        chefs = Chef.objects.filter().order_by("-heart_number")

        serializer = self.serializer_class(chefs, many=True)

        return Response(serializer.data)
