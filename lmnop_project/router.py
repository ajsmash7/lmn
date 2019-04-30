from lmn import viewsets
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'show', viewsets.ShowViewSet)