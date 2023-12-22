from datetime import datetime
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncDate
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response, APIView
from django.db.utils import IntegrityError

from likes.models import LikeModel
from likes.serializers import LikeStatsSerializer


class LikeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        is_liked = False
        post_id = request.query_params.get("post_id")
        try:
            like = LikeModel.objects.get(post_id=post_id, user_id=request.user.id)
            like.delete()
        except LikeModel.DoesNotExist:
            try:
                LikeModel.objects.create(
                    post_id=post_id,
                    user_id=request.user.id
                )
                is_liked = True
            except IntegrityError:
                raise APIException(f"Post with id {post_id} not found!")
        return Response({"msg": f"You successfully {'' if is_liked else 'dis'}liked post with id {post_id}"})


class LikeStatsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeStatsSerializer

    def get(self, request):
        date_from = request.query_params.get("date_from", datetime(1980, 1, 1))
        if isinstance(date_from, str):
            date_from = datetime.strptime(date_from, "%Y-%m-%d")
        date_to = request.query_params.get("date_to", timezone.now())
        if isinstance(date_to, str):
            date_to = datetime.strptime(date_to, "%Y-%m-%d")
        like_stats = LikeModel.objects.filter(
            user=request.user, created_at__range=[date_from, date_to]
        ).annotate(
            date=TruncDate('created_at')
        ).values("date").annotate(
            likes_count=Count("id")
        ).order_by('-date')
        return Response(self.serializer_class(like_stats, many=True).data)
