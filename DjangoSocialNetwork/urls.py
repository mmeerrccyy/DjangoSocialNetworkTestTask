from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls"), name="user-endpoints"),
    path("api/posts/", include("posts.urls"), name="posts-endpoints"),
    path("api/like/", include("likes.urls"), name="posts-endpoints"),

]
