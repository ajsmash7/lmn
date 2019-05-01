from rest_framework import viewsets, renderers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Show
from .serializer import ShowSerializer
import requests
from lmnop_project.settings import api_key

# Originally tried to import the json data from api
baseURL = ('http://api.eventful.com/json/events/search?app_key=' + api_key + '&q=music&location=Minneapolis')

""" Create Viewsets of the Serializers, to route to the API extension"""

# use rest framework to create a view for all show object queryset from serializer class
class ShowViewSet(viewsets.ModelViewSet):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer

    # set the action method to post, detail to true, and browsableAPI renderer if a renderer class is needed
    # browsableAPI chooses the renderer most appropriate for the data
    @action(methods=['post'], detail=True, renderer_classes=[renderers.BrowsableAPIRenderer])

    # originally was going to call a get data method to read in the json data from the url
    def get_data(self, request, *args, **kwargs):
        '''Get all show events from api'''

        r = requests.get(baseURL + '&keywords=' + request)
        json = r.json()
        serializer = ShowSerializer(data=json)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

