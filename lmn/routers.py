from .viewsets import ShowViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('show', ShowViewSet)