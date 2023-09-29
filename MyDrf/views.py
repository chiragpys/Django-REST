from django.shortcuts import render
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle


# Create your views here.

@api_view(['GET'])
@throttle_classes([AnonRateThrottle])
def example_view(request):
    content = {
        'status': 'request was permitted'
    }
    return Response(content)