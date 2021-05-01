from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics, mixins, viewsets
from main.serializers import MovieDetailSerializer, MovieListSerializer, ScoreSerializer
from rest_framework.response import Response
from rest_framework import status
from main.models import Score, Movie
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404


# class MovieDetailView(mixins.ListModelMixin,
#                       mixins.CreateModelMixin,
#                       viewsets.GenericViewSet):
#     serializer_class = MovieDetailSerializer
#

# class MovieListView(viewsets.ViewSet):
#     serializer_class = MovieListSerializer
#     pagination_class = LimitOffsetPagination
#
#     def list(self, request):
#         queryset = Movie.objects.all()
#         serializer = self.serializer_class(queryset, many=True)
#         return Response(serializer.data)


# def movie_score_update_view(movie_id):
#     obj = Movie.objects.get_movie(pk=movie_id).first()
#     obj.avg_score = Score.objects.avg_score(pk=movie_id)
#     obj.cnt_voters = Score.objects.get_cnt_voters(pk=movie_id)
#     obj.save()
#     return obj


class ScoreView(APIView):
    serializer_class = ScoreSerializer

    def get(self, request, movie_id):
        obj = Score.objects.get_movie_score_by_user(user_id=request.user.id, movie_id=movie_id).first()
        if obj:
            serializer = self.serializer_class(obj)
            return Response(serializer.data)
        return Response({'error': 'You have not yet rated the movie.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, movie_id):
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

    @staticmethod
    def delete(request, movie_id):
        saved_score = Score.objects.get_movie_score_by_user(user_id=request.user.id, movie_id=movie_id).first()
        if saved_score:
            saved_score.delete()
            # movie_score_update_view(movie_id)
            return Response({'status_message': 'Movie rating has been removed successfully.'},
                            status=status.HTTP_200_OK)
        return Response({'error': 'There is no such movie.'}, status=status.HTTP_400_BAD_REQUEST)
