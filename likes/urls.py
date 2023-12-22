from django.urls import path

from .views import LikeView, LikeStatsView


urlpatterns = [
    path("", LikeView.as_view(), name="like"),
    path("stats", LikeStatsView.as_view(), name="like-stats")
]
