from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from auth_.models import Profile, MainUser
from account.serializers import ProfileDetailSerializer, ProfileUpdateSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from account.permissions import IsOwner, IsOwnerOrAdmin


class UserListView(generics.ListAPIView):
    queryset = MainUser.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = UserSerializer


class UserRetrieveView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProfileDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = Profile.objects.get(user=kwargs['pk'])
        except Profile.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserUpdateView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated, IsOwner,)
    serializer_class = ProfileUpdateSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data
        data['user'] = request.user.id
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class UserDeleteView(mixins.DestroyModelMixin,
                     generics.GenericAPIView):
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin,)
    serializer_class = ProfileUpdateSerializer

    def delete(self, request, *args, **kwargs):
        try:
            instance = Profile.objects.get(user=kwargs['pk'])
        except Profile.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance)
        # user = MainUser.objects.get(id=kwargs['pk'])
        # user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
