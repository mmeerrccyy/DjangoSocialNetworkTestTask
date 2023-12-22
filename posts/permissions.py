from rest_framework import permissions
from rest_framework.exceptions import APIException
from rest_framework.views import status

from posts.models import PostModel


class IsUserHasAccessPermission(permissions.BasePermission):
    message = "You don't have permissions to delete and update this post!"

    def has_permission(self, request, view):
        if request.method in ["PUT", "DELETE"] and request.user.is_authenticated:
            post_id = request.query_params["post_id"]
            try:
                post = PostModel.objects.get(id=post_id)
            except PostModel.DoesNotExist:
                raise APIException(f"Post with id {post_id} not found!", status.HTTP_404_NOT_FOUND)
            return post.user_id == request.user.id
        return True
