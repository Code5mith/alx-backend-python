from django.shortcuts import render

# Create your views here.
# messaging/views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    username = user.username
    user.delete()
    return Response(
        {"message": f"User {username} and related data deleted successfully."},
        status=status.HTTP_200_OK
    )
