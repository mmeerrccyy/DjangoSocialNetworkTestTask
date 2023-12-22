from django.db import models
from posts.models import PostModel
from users.models import CustomUserModel


# Create your models here.

class LikeModel(models.Model):

    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
