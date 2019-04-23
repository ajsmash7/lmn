from django.shortcuts import render
import requests


def homepage(request):
    return render(request, 'lmn/home.html')

