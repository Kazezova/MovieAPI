from django.shortcuts import render
from rest_framework import generics, mixins, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from auth_.serializers import CreateUserSerializer
from auth_.models import MainUser
from rest_framework.permissions import IsAuthenticated, AllowAny


# class UserView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = ProfileSerializer
#     queryset = Profile.objects.get_queryset()

class UserRegisterView(generics.CreateAPIView):
    queryset = MainUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CreateUserSerializer


# class UserRetrieveView(generics.RetrieveAPIView):
#     queryset = Profile.objects.all()
#     permission_classes = (AllowAny,)
#     serializer_class = ProfileSerializer
