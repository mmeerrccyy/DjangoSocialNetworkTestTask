from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response

from .models import PostModel
from .permissions import IsUserHasAccessPermission
from .serializers import PostSerializer


class PostView(APIView):
    permission_classes = [IsUserHasAccessPermission]

    def get_serializer_context(self):
        return {"user": self.request.user}

    def get(self, request):
        public_id = request.query_params.get("user_public_id")
        if public_id:
            return Response(PostSerializer(PostModel.objects.filter(user__public_id=public_id), many=True).data)
        return Response(PostSerializer(PostModel.objects.all(), many=True).data)

    def post(self, request):
        serializer = PostSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request):
        post_id = request.query_params.get("post_id")
        post = PostModel.objects.get(id=post_id)
        serializer = PostSerializer(post, data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request):
        post_id = request.query_params.get("post_id")
        PostModel.objects.get(id=post_id).delete()
        return Response({"msg": f"Post with id {post_id} deleted!"})
