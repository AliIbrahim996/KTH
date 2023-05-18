from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Chef
from core.serializer import ChefListSerializer


class ChefView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChefListSerializer

    def get(self, request, chef_id=None):
        is_delivery = request.query_params.get('is_delivery', False)
        if chef_id is not None:
            chef = Chef.objects.filter(id=chef_id)
        elif is_delivery == 1:
            chef = Chef.objects.filter(is_delivery=True)
        else:
            chef = Chef.objects.filter(is_delivery=False)

        context = {"user_id": request.user.id}

        serializer = self.serializer_class(chef, many=True, context=context)

        return Response(serializer.data, status=status.HTTP_200_OK)


class BestChefsView(ChefView):
    serializer_class = ChefListSerializer

    def get(self, request, *args, **kwargs):
        chefs = Chef.objects.filter().order_by("-heart_number")

        serializer = self.serializer_class(chefs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
