from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework import permissions
from core.models import WishList, Meal
from core.serializer import WishListSerializer


class WishListAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        customer_id = request.user.id
        wish_list = WishList.objects.filter(customer=customer_id)
        context = {"user_id": request.user.id}
        wish_list_serializer = WishListSerializer(wish_list, many=True, context=context)
        return Response({
            "wish_list": wish_list_serializer.data,
        }, status=status.HTTP_200_OK)

    def post(self, request, meal_id=None):
        customer_id = request.user.id
        wish_list = WishList.objects.filter(customer=customer_id, meal=meal_id)
        if not wish_list:
            try:
                meal = Meal.objects.get(id=meal_id)
                WishList.objects.create(meal=meal, customer=request.user)
                return Response({
                    "meal added to the wish list",
                }, status=status.HTTP_200_OK)
            except Meal.DoesNotExist:
                return Response({
                    "no such meal",
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "meal already exist in the wish list",
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, meal_id=None):
        customer_id = request.user.id
        wish_list = WishList.objects.filter(customer=customer_id, meal=meal_id)
        if wish_list:
            wish_list.delete()
            return Response({
                "meal removed from wish list",
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "meal not in the wish list",
            }, status=status.HTTP_400_BAD_REQUEST)


class WishListViewSet(ModelViewSet):
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
