from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from auth_.serializers import UserCreateSerializer
from auth_.models import MainUser
from rest_framework.permissions import AllowAny
import logging

logger = logging.getLogger(__name__)


class UserCreatViewSet(viewsets.ViewSet):
    queryset = MainUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserCreateSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Registered new user, ID: {serializer.data['id']}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.error(f"Cannot registered new user, errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
