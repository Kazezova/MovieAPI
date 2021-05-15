from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from django.utils import timezone
from rest_framework import generics, mixins, viewsets
from rest_framework.decorators import action, api_view, permission_classes, parser_classes
from main.serializers import *
from rest_framework.response import Response
from rest_framework import status
from main.models import Score, Movie, FavoriteWatched, Review, Genre, MPAA
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from main.permissions import IsAdminUserOrReadOnly
from account.permissions import IsOwnerOrAdmin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from main.filters import MovieFilter
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
import logging

logger = logging.getLogger(__name__)


class MovieViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    pagination_class = LimitOffsetPagination
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('title', 'original_title', 'tagline', 'short_description', 'full_description',)
    ordering_fields = ('id', 'title', 'avg_score', 'release_date', 'cnt_voters',)
    filterset_class = MovieFilter
    parser_classes = (FormParser, MultiPartParser, JSONParser,)

    def get_queryset(self):
        return Movie.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        return MovieDetailSerializer

    def retrieve(self, request, pk=None):
        movie = Movie.objects.get_movie(pk=pk).first()
        if movie:
            serializer = MovieDetailSerializer(movie)
            logger.debug(f'Retrieved Movie object, ID: {pk}')
            return Response(serializer.data)
        logger.debug(f'Trying to get nonexistent Movie object, ID: {pk}')
        return Response({'error': 'There is no such movie.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes((IsAdminUser,))
@parser_classes((FormParser, MultiPartParser, JSONParser,))
def movie_crud(request):
    if request.method == 'GET':
        movie = Movie.objects.get_movie(pk=request.data['id']).first()
        if movie:
            serializer = MovieDetailSerializer(movie)
            logger.debug(f"Retrieved Movie object, ID: {request.data['id']} by staff with ID: {request.user.id}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.debug(f"Trying to get nonexistent Movie object, ID: {request.data['id']} ")
        return Response({'error': 'There is no such movie.'}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'POST':
        data = request.data
        serializer = MovieCreateOrUpdateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Created Movie object, ID: {request.data['id']} by staff with ID: {request.user.id}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.error(f"Movie object cannot created, errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        movie = Movie.objects.get_movie(pk=request.data['id']).first()
        if movie:
            serializer = MovieCreateOrUpdateSerializer(instance=movie, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Updated Movie object, ID: {request.data['id']} by staff with ID: {request.user.id}")
                return Response(serializer.data, status=status.HTTP_200_OK)
            logger.error(f"Movie object cannot updated, errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        logger.warning(f"Trying to update nonexistent Movie object, ID: {request.data['id']}")
        return Response({'error': 'There is no such movie.'}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'DELETE':
        movie = Movie.objects.get_movie(pk=request.data['id']).first()
        if movie:
            movie.delete()
            logger.info(f"Deleted Movie object, ID: {request.data['id']} by staff with ID: {request.user.id}")
            return Response({'status_message': 'Movie has been removed successfully.'}, status=status.HTTP_200_OK)
        logger.warning(f"Trying to delete nonexistent Movie object, ID: {request.data['id']}")
        return Response({'error': 'There is no such movie.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((AllowAny,))
def mpaa_get(request):
    if request.method == 'GET':
        queryset = MPAA.objects.all()
        serializer = MPAASerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
def latest(request):
    queryset = Movie.objects.latest()
    serializer = MovieListSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
def top_rated(request):
    queryset = Movie.objects.top_rated()
    serializer = MovieListSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
def genre_get(request):
    if request.method == 'GET':
        queryset = Genre.objects.all()
        serializer = GenreSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProducerApiView(generics.CreateAPIView,
                      generics.RetrieveAPIView,
                      generics.UpdateAPIView,
                      generics.DestroyAPIView):
    queryset = Producer.objects.all()
    serializer_class = ProducerDetailSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    parser_classes = (FormParser, MultiPartParser, JSONParser,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status_message': 'Producer has been removed successfully.'},
                        status=status.HTTP_204_NO_CONTENT)


class ScoreViewSet(viewsets.ViewSet):
    serializer_class = ScoreSerializer

    @action(methods=['GET'], detail=False, permission_classes=(IsAuthenticated,))
    def retrieve(self, request, movie_id=None):
        obj = Score.objects.get_movie_score_by_user(user_id=request.user.id, movie_id=movie_id).first()
        if obj:
            serializer = self.serializer_class(obj)
            logger.debug(f"Retrieved Score object, ID: {obj.id}")
            return Response(serializer.data)
        logger.warning(f"Trying to get nonexistent Score object.")
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
            logger.info(f"Score object created/updated.")
            # movie_score_update_view(movie_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.warning(f"Score object cannot created/updated, errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['DELETE'], detail=False, permission_classes=(IsAuthenticated,))
    def delete(self, request, movie_id=None):
        saved_score = Score.objects.get_movie_score_by_user(user_id=request.user.id, movie_id=movie_id).first()
        if saved_score:
            saved_score.delete()
            # movie_score_update_view(movie_id)
            logger.info(f"Score object deleted.")
            return Response({'status_message': 'Movie rating has been removed successfully.'},
                            status=status.HTTP_200_OK)
        logger.warning(f"Trying to delete nonexistent Score object.")
        return Response({'error': 'There is no such movie.'}, status=status.HTTP_400_BAD_REQUEST)


class FavoriteViewSet(viewsets.ViewSet):
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = FavoriteWatched.objects.get_favorite_list(request.user.id)
        serializer = FavoriteWatchedSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        movie_id = request.data['movie']
        saved = FavoriteWatched.objects.get_relation(user_id=request.user.id, movie_id=movie_id).first()
        if saved:
            data = {
                "favorite": True,
            }
            serializer = FavoriteWatchedManipulateSerializer(instance=saved, data=data, partial=True)
        else:
            data = {
                "user_id": request.user.id,
                "movie_id": movie_id,
                "favorite": True,
                "watched": False
            }
            serializer = FavoriteWatchedManipulateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status_message': 'Movie has been successfully added to favorites.'},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        movie_id = request.data['movie']
        saved = FavoriteWatched.objects.get_relation(user_id=request.user.id, movie_id=movie_id).first()
        if saved:
            data = {
                "favorite": False,
            }
            serializer = FavoriteWatchedManipulateSerializer(instance=saved, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status_message': 'Movie has been successfully removed from the favorites.'},
                                status=status.HTTP_200_OK)
        return Response({'error': 'There is no such favorite.'}, status=status.HTTP_400_BAD_REQUEST)


class WatchedViewSet(viewsets.ViewSet):
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = FavoriteWatched.objects.get_watched_list(request.user.id)
        serializer = FavoriteWatchedSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        movie_id = request.data['movie']
        saved = FavoriteWatched.objects.get_relation(user_id=request.user.id, movie_id=movie_id).first()
        if saved:
            data = {
                "watched": True,
            }
            serializer = FavoriteWatchedManipulateSerializer(instance=saved, data=data, partial=True)
        else:
            data = {
                "user_id": request.user.id,
                "movie_id": movie_id,
                "favorite": False,
                "watched": True
            }
            serializer = FavoriteWatchedManipulateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status_message': 'Movie has been successfully added to watched list.'},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        movie_id = request.data['movie']
        saved = FavoriteWatched.objects.get_relation(user_id=request.user.id, movie_id=movie_id).first()
        if saved:
            data = {
                "watched": False,
            }
            serializer = FavoriteWatchedManipulateSerializer(instance=saved, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status_message': 'Movie has been successfully removed from the watched list.'},
                                status=status.HTTP_200_OK)
        return Response({'error': 'There is no such movie in watched list.'}, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.GenericViewSet):

    def list(self, request, movie_id=None):
        queryset = Review.objects.get_movie_reviews(movie_id=movie_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ReviewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        elif queryset:
            serializer = ReviewSerializer(queryset, many=True)
            logger.debug(f"Review objects retrieved, for movie ID: {movie_id}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.debug(f"This Movie object has no reviews yet, ID: {movie_id}.")
        return Response({'error': 'This movie has no reviews yet.'}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['POST'], detail=False, permission_classes=(IsAuthenticated,))
    def create(self, request, movie_id=None):
        if request.data.get('review_id', 0) != 0:
            saved_review = Review.objects.get_review(request.data['review_id']).first()
            if saved_review:
                data = {
                    "updated_date": timezone.now(),
                    "content": request.data['content']
                }
                serializer = ReviewManipulateSerializer(instance=saved_review, data=data, partial=True)
            else:
                logger.warning(f"Trying to update nonexistent Review object, ID: {request.data['review_id']}")
                return Response({'error': 'There is no such review.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            content = request.data.get('content', 0)
            if content:
                data = {
                    "author_id": request.user.id,
                    "movie_id": movie_id,
                    "created_date": timezone.now(),
                    "updated_date": None,
                    "content": request.data['content']
                }
                serializer = ReviewManipulateSerializer(data=data)
            else:
                logger.error(f"Review object cannot created/updated, errors: content is required.")
                return Response({"errors": "content is required."}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Review object has been created/updated, ID: {serializer.data['id']}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.error(f"Review object cannot created/updated, errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['DELETE'], detail=False, permission_classes=(IsOwnerOrAdmin,))
    def delete(self, request, movie_id=None):
        saved_review = Review.objects.get_review(request.data['review_id']).first()
        if saved_review:
            if self.check_object_permissions(self.request, saved_review):
                saved_review.delete()
                logger.info(f"Review object has been deleted, ID: {request.data['review_id']}")
                return Response({'status_message': 'Review has been removed successfully.'},
                                status=status.HTTP_200_OK)
            logger.warning(
                f"Review object cannot deleted, ID: {request.data['review_id']} by user ID: {request.user.id}")
            return Response({'detail': 'You do not have permission to perform this action.'},
                            status=status.HTTP_400_BAD_REQUEST)
        logger.warning(f"Trying to delete nonexistent Review object, ID: {request.data['review_id']}")
        return Response({'error': 'There is no such review.'}, status=status.HTTP_400_BAD_REQUEST)
