from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics, mixins, viewsets
from rest_framework.decorators import action
from main.serializers import MovieDetailSerializer, MovieListSerializer, ScoreSerializer
from rest_framework.response import Response
from rest_framework import status
from main.models import Score, Movie
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from main.filters import MovieFilter


class MovieViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    pagination_class = LimitOffsetPagination
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('title', 'original_title', 'tagline', 'short_description', 'full_description',)
    ordering_fields = ('id', 'title', 'avg_score', 'release_date', 'cnt_voters',)
    filterset_class = MovieFilter

    def get_queryset(self):
        return Movie.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        return MovieDetailSerializer

    # filter_backends = (DjangoFilterBackend,)

    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return MovieListSerializer
    #     return MovieDetailSerializer

    # @action(methods=['GET'], detail=False, permission_classes=(AllowAny,))
    # def movie_list(self, request):
    #     queryset = Movie.objects.all()
    #     serializer_class = MovieListSerializer
    #
    # def list(self, request):
    #     serializer = MovieListSerializer(self.queryset, many=True)
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, pk=None):
    #     movie = get_object_or_404(self.queryset, pk=pk)
    #     serializer = MovieDetailSerializer(movie)
    #     return Response(serializer.data)


class ScoreViewSet(viewsets.ViewSet):
    serializer_class = ScoreSerializer

    @action(methods=['GET'], detail=False, permission_classes=(IsAuthenticated,))
    def retrieve(self, request, movie_id=None):
        obj = Score.objects.get_movie_score_by_user(user_id=request.user.id, movie_id=movie_id).first()
        if obj:
            serializer = self.serializer_class(obj)
            return Response(serializer.data)
        return Response({'error': 'You have not yet rated the movie.'}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['POST'], detail=False, permission_classes=(IsAuthenticated,))
    def create(self, request, movie_id=None):
        saved_score = Score.objects.get_movie_score_by_user(user_id=request.user.id, movie_id=movie_id).first()
        if saved_score:
            serializer = self.serializer_class(instance=saved_score, data=request.data, partial=True)
        else:
            data = {
                "user_id": request.user.id,
                "movie_id": movie_id,
                "score": request.data['score']
            }
            serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            # movie_score_update_view(movie_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['DELETE'], detail=False, permission_classes=(IsAuthenticated,))
    def delete(self, request, movie_id=None):
        saved_score = Score.objects.get_movie_score_by_user(user_id=request.user.id, movie_id=movie_id).first()
        if saved_score:
            saved_score.delete()
            # movie_score_update_view(movie_id)
            return Response({'status_message': 'Movie rating has been removed successfully.'},
                            status=status.HTTP_200_OK)
        return Response({'error': 'There is no such movie.'}, status=status.HTTP_400_BAD_REQUEST)
