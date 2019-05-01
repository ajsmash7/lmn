from .viewsets import ShowViewSet
from rest_framework import routers

""" Route the API viewsets using Django rest framework DefaultRouter"""

# url extension for the API Show Viewset is /show/
# so to post a show to the app api would use base url + /api/show
router = routers.DefaultRouter()
router.register('show', ShowViewSet)
