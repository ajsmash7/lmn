from rest_framework import viewsets, renderers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Show
from .serializer import ShowSerializer
import requests
from lmnop_project.settings import api_key

baseURL = ('http://api.eventful.com/json/events/search?app_key=' + api_key + '&q=music&location=Minneapolis')


class ShowViewSet(viewsets.ModelViewSet):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer

    @action(methods=['post'], detail=True, renderer_classes=[renderers.BrowsableAPIRenderer])
    def get_data(self, request, *args, **kwargs):
        '''Get all show events from api'''

        r = requests.get(baseURL + '&keywords=' + request)
        json = r.json()
        serializer = ShowSerializer(data=json)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

