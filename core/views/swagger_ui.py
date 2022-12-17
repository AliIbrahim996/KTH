from django.views.generic import TemplateView
from rest_framework import permissions
from rest_framework.decorators import permission_classes


@permission_classes([permissions.AllowAny])
class SwaggerUITemplateView(TemplateView):
    """A class overrides permission for API Swagger Documentation Page"""