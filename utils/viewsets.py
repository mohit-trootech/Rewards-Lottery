# Custom Modified Viewsets
from rest_framework.viewsets import ModelViewSet


class SoftDestroyModelViewset(ModelViewSet):
    """customized model for `Soft Delete` method & required `status` fields"""

    def perform_destroy(self, instance):
        instance.soft_delete()
