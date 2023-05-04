# from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import AllowAny

from app_custom_user.models import CustomUser
from app_custom_user.serializers import CustomUserSerializer

# # from user.permissions import SuperMan  #  временно не актуально
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response


class UserCreateView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        user = request.data
        serializer = CustomUserSerializer(data=user, context={'request': request})
        if serializer.is_valid():
            user_saved = serializer.save(password=make_password(user['password']))
            return Response('success')
        return Response({
            'error': 'Error 4to-to-tam'},
            status=406)
