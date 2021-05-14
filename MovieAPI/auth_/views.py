from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from auth_.serializers import UserCreateSerializer
from auth_.models import MainUser
from rest_framework.permissions import AllowAny


class UserCreatViewSet(viewsets.ViewSet):
    queryset = MainUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserCreateSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
