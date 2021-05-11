from django.urls import path, include
from main import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('movies', views.MovieViewSet, basename='main')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:movie_id>/score', views.ScoreViewSet.as_view({
        'get': 'retrieve',
        'post': 'create',
        'delete': 'delete',
    })),
    # path('<int:movie_id>/score', views.ScoreView.as_view())
]
