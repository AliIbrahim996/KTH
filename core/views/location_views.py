from core.models import Location
from core.serializer import LocationSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from core.serializer.location_serializer import UserLocationSerializer

class LocView(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LocationSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.user:
            context.update({"user_id": self.request.user.id})
        return context


class LocationView(viewsets.ModelViewSet, LocView):

    def get_queryset(self):
        if 'pk' in self.kwargs:
            return Location.objects.filter(pk=self.kwargs['pk']).defer("customer")
        return Location.objects.none()

    def create(self, request, *args, **kwargs):
        try:
            res = super().create(request, *args, **kwargs)
            res.data.update({"msg": "New location is created!"})
            return res
        except Exception as e:
            return Response({"msg:" + str(e)}, status=HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        res = super().partial_update(request, *args, **kwargs)
        res.data.update({"msg": "Location is updated!"})
        return res

    def update(self, request, *args, **kwargs):
        res = super().update(request, *args, **kwargs)
        res.data.update({"msg": "Location is updated!"})
        return res

    def destroy(self, request, *args, **kwargs):
        res = super().destroy(request, *args, **kwargs)
        return Response({"msg: Location is deleted!"}, status=HTTP_200_OK)

class UserLocationView(viewsets.ReadOnlyModelViewSet, LocView):

    def get_queryset(self):
        if self.request:
            return Location.objects.filter(customer__id=self.request.user.id).defer("customer")
        return Location.objects.none()


class NewUserLocationView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        qs = UserLocation.objects.filter(user=request.user)
        serializer = UserLocationSerializer(qs, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self,request, *args, **kwargs):
        serializer = UserLocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def patch(self,request, *args, **kwargs):
        location_id = request.query_params.get('id')
        location_object = UserLocation.objects.get(id=location_id)
        serializer = UserLocationSerializer(location_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
