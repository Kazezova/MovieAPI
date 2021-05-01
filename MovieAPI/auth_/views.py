from rest_framework import generics, mixins, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from auth_.serializers import UserCreateSerializer
from auth_.models import MainUser
from rest_framework.permissions import AllowAny


class UserCreateView(generics.CreateAPIView):
    queryset = MainUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserCreateSerializer
