from core.models import Location
from core.serializer import LocationSerializer
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK


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
