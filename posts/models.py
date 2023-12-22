from django.db import models

from users.models import CustomUserModel


# Create your models here.


class PostModel(models.Model):

    text = models.TextField("Post's text")
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, null=False, blank=False)
