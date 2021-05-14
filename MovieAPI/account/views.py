from rest_framework import generics, mixins
from rest_framework.permissions import AllowAny, IsAdminUser
from account.permissions import IsOwner, IsOwnerOrAdmin
from auth_.models import Profile, MainUser
from account.serializers import ProfileDetailSerializer, ProfileUpdateSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser


class UserListView(generics.ListAPIView):
    queryset = MainUser.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer


class UserRetrieveView(generics.RetrieveAPIView):
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
    permission_classes = (IsOwner,)
    serializer_class = ProfileUpdateSerializer
    parser_classes = (FormParser, MultiPartParser, JSONParser)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        try:
            instance = Profile.objects.get(user=kwargs['pk'])
            self.check_object_permissions(self.request, instance)
        except Profile.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        data['user'] = request.user.id
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class UserDeleteView(generics.GenericAPIView,
                     mixins.DestroyModelMixin):
    permission_classes = (IsOwnerOrAdmin,)
    serializer_class = ProfileUpdateSerializer

    def delete(self, request, *args, **kwargs):
        try:
            instance = Profile.objects.get(user=kwargs['pk'])
            self.check_object_permissions(self.request, instance)
        except Profile.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance)

        # user = MainUser.objects.get(id=kwargs['pk'])
        # user.delete()

        return Response({"detail": "User has been removed successfully."}, status=status.HTTP_200_OK)
