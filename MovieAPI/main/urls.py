from django.urls import path, include
from main import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('movies', views.MovieViewSet, basename='main')
router.register('favorites', views.FavoriteViewSet, basename='main')
router.register('watched', views.WatchedViewSet, basename='main')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:movie_id>/score', views.ScoreViewSet.as_view({
        'get': 'retrieve',
        'post': 'create',
        'delete': 'delete',
    })),
    path('<int:movie_id>/reviews', views.ReviewViewSet.as_view({
        'get': 'list',
        'post': 'create',
        'delete': 'delete',
    })),
    path('crud', views.movie_crud),
    path('mpaa', views.mpaa_get),
    path('genre', views.genre_get),
    path('producer/<int:pk>', views.ProducerApiView.as_view()),
    path('producers', views.ProducerListView.as_view()),
    path('latest', views.latest),
    path('top_rated', views.top_rated)
]
