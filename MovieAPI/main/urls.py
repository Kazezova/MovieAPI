from django.urls import path
from main import views
urlpatterns = [
    path('<int:movie_id>/score', views.ScoreView.as_view()),
]