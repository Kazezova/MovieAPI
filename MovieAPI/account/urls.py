from django.urls import path
from account.views import UserListView, UserRetrieveView, UserUpdateView, UserDeleteView

urlpatterns = [
    path('all/', UserListView.as_view()),
    path('<int:pk>/', UserRetrieveView.as_view()),
    path('<int:pk>/update', UserUpdateView.as_view()),
    path('<int:pk>/delete', UserDeleteView.as_view()),
]
