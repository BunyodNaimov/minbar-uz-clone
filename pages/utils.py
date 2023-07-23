from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from pages.models import Comment, CommentLike, PostLike
from pages.serializers import CommentLikeSerializer, PostLikeSerializer


class PostLikeView(CreateAPIView):
    serializer_class = PostLikeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        post = serializer.validated_data.get('post')
        if not post:
            return Response({'error': 'Post object not found'}, status=status.HTTP_400_BAD_REQUEST)
        if post.author == user:
            return Response({'error': 'You cannot like or dislike your own post'}, status=status.HTTP_400_BAD_REQUEST)
        value = serializer.validated_data.get('value')
        try:
            like = PostLike.objects.get(user=user, post=post)
            if like.value == 1 and value == -1:
                # Если пользователь нажал на кнопку дизлайка, а потом на кнопку лайка, то мы убираем лайк и добавляем дизлайк
                like.post.likes -= 1
                like.post.dislikes += 1
                like.value = -1
                like.post.save()
                like.save()
            elif like.value == -1 and value == 1:
                # Если пользователь нажал на кнопку лайка, а потом на кнопку дизлайка, то мы убираем дизлайк и добавляем лайк
                like.post.dislikes -= 1
                like.post.likes += 1
                like.value = 1
                like.post.save()
                like.save()
            elif like.value == 1 and value == 1:
                # Если пользователь нажал на кнопку лайка дважды, то мы отменяем свой голос
                like.post.likes -= 1
                like.value = 0
                like.post.save()
                like.delete()
            elif like.value == -1 and value == -1:
                # Если пользователь нажал на кнопку дизлайка дважды, то мы отменяем свой голос
                like.post.dislikes -= 1
                like.value = 0
                like.post.save()
                like.delete()
        except PostLike.DoesNotExist:
            serializer.save(user=user)
            if value == 1:
                post.likes += 1
            elif value == -1:
                post.dislikes += 1
            post.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentLikeView(CreateAPIView):
    serializer_class = CommentLikeSerializer

    @swagger_auto_schema(request_body=CommentLikeSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        comment = Comment.objects.filter(id=kwargs.get('comment_id')).first()
        if not comment:
            return Response({'error': 'Comment not found'}, status=status.HTTP_400_BAD_REQUEST)

        if comment.author == user:
            return Response({'error': 'You cannot like or dislike your own comment'},
                            status=status.HTTP_400_BAD_REQUEST)

        value = serializer.validated_data.get('value')

        try:
            like = CommentLike.objects.get(user=user, comment=comment)
            if like.value == 1 and value == -1:
                # Если пользователь нажал на кнопку дизлайка, а потом на кнопку лайка, то мы убираем лайк и добавляем дизлайк
                like.comment.likes -= 1
                like.comment.dislikes += 1
                like.value = -1
                like.comment.save()
                like.save()
            elif like.value == -1 and value == 1:
                # Если пользователь нажал на кнопку лайка, а потом на кнопку дизлайка, то мы убираем дизлайк и добавляем лайк
                like.comment.dislikes -= 1
                like.comment.likes += 1
                like.value = 1
                like.comment.save()
                like.save()
            elif like.value == 1 and value == 1:
                # Если пользователь нажал на кнопку лайка дважды, то мы отменяем свой голос
                like.comment.likes -= 1
                like.value = 0
                like.comment.save()
                like.delete()
            elif like.value == -1 and value == -1:
                # Если пользователь нажал на кнопку дизлайка дважды, то мы отменяем свой голос
                like.comment.dislikes -= 1
                like.value = 0
                like.comment.save()
                like.delete()
        except CommentLike.DoesNotExist:
            serializer.save(user=user, comment=comment)
            if value == 1:
                comment.likes += 1
            elif value == -1:
                comment.dislikes += 1
            comment.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
