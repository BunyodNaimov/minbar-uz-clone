from rest_framework import status, permissions
from rest_framework.generics import ListAPIView, ListCreateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pages.models import Page, Post, PageInteraction, PostLike, Comment, CommentLike
from pages.serializers import PageSerializer, PostSerializer, BlockedPageSerializer, PostCreateSerializer, \
    PostLikeSerializer, CommentSerializer, CommentLikeSerializer
from pages.utils import CommentLikeView


class PageListAPIVew(ListAPIView):
    serializer_class = PageSerializer

    def get_queryset(self):
        return Page.objects.exclude(page_interaction__user=self.request.user)


class PostListCreateAPIView(ListCreateAPIView):
    serializer_class = PostSerializer

    def get_serializer_class(self):
        if self.request.method in ['POST']:
            return PostCreateSerializer
        return PostSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        user_id = self.request.user.id
        uninteresting_pages = PageInteraction.objects.filter(user_id=user_id, is_uninteresting=True).values_list(
            'page_id', flat=True)
        return Post.objects.exclude(author_id__in=uninteresting_pages)


class PostLikeAPIView(CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)


class CommentLikeAPIView(CommentLikeView):
    permission_classes = [IsAuthenticated]


class MarkPageUninterested(APIView):
    """Пометить как «Неинтересно»"""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        page = Page.objects.get(id=pk)
        is_uninteresting = PageInteraction(user=request.user, page=page, is_uninteresting=True)
        is_uninteresting.save()
        serializer = BlockedPageSerializer(is_uninteresting)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UnmarkPageUninteresting(APIView):
    """Снять пометку «Неинтересно»"""

    def post(self, request, *args, **kwargs):
        page_id = kwargs.get('pk')
        user_id = kwargs.get('pk')

        page_interaction = PageInteraction.objects.filter(page_id=page_id, user_id=user_id).first()
        if page_interaction:
            page_interaction.is_uninteresting = False
            page_interaction.save()
            return Response({'status': 'success'})
        else:
            return Response({'status': 'error', 'message': 'Page interaction not found.'},
                            status=status.HTTP_404_NOT_FOUND)


class UninterestingPagesList(ListAPIView):
    serializer_class = PageSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = PageInteraction.objects.filter(user_id=user_id, is_uninteresting=True).values_list('page_id',
                                                                                                      flat=True)
        return Page.objects.filter(id__in=queryset)


class CommentListCreateAPIView(ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post__id=post_id)

    def post(self, request, post_id):  # noqa
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            post = Post.objects.get(id=post_id)
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
