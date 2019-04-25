from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Show
from .serializer import ShowSerializer


def homepage(request):
    return render(request, 'lmn/home.html')


@api_view(['GET', 'POST'])
def get_api_data(request, format=None):
    '''Get all show events from api'''

    if request.method == 'GET':
        events = Show.objects.all()
        events.show_headliner.all()
        serializer = ShowSerializer(events, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ShowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def show_detail(request, show_pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """

    try:
        event = Show.objects.get(pk=show_pk)
    except Show.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ShowSerializer(event)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ShowSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)