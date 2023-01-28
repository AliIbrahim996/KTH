from core.models import Location, User
from core.serializer import LocationSerializer
from rest_framework import viewsets
from rest_framework import permissions


class LocView(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LocationSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request:
            context.update({"user_id": self.request.user.id})
        return context


class LocationView(viewsets.ModelViewSet, LocView):

    def get_queryset(self):
        if 'pk' in self.kwargs:
            return Location.objects.filter(pk=self.kwargs['pk'])
        return Location.objects.none()

    def create(self, request, *args, **kwargs):
        res = super().create(request, *args, **kwargs)
        res.data.update({"msg": "New location is created!"})
        return res

    def partial_update(self, request, *args, **kwargs):
        res = super().partial_update(request, *args, **kwargs)
        res.data.update({"msg": "Location is updated!"})
        return res


class UserLocationView(viewsets.ReadOnlyModelViewSet, LocView):

    def get_queryset(self):
        if self.request:
            return Location.objects.filter(customer__id=self.request.user.id)
        return Location.objects.none()
