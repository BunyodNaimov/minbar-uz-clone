from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework import status, permissions, filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from categories.serializers import CategorySerializer
from pages.models import Page, Post, PageInteraction, Comment
from pages.serializers import PageSerializer, PostSerializer, BlockedPageSerializer, PostCreateSerializer, \
    CommentSerializer, PageDetailSerializer
from pages.utils import CommentLikeView, PostLikeView
from pagination import CustomPageNumberPagination


class PageListAPIVew(ListAPIView):
    serializer_class = PageSerializer

    def get_queryset(self):
        return Page.objects.exclude(page_interaction__user=self.request.user)


class PageDetailView(RetrieveUpdateAPIView):
    queryset = Page.objects.all()
    serializer_class = PageDetailSerializer

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('position',)
    search_fields = ('title', 'description', 'position')
    ordering_fields = ('position', 'created_at')
    pagination_class = CustomPageNumberPagination


class PostListCreateAPIView(ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('category',)
    search_fields = ('title', 'description', 'categories')
    ordering_fields = ('categories', 'created_at')
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return Post.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST']:
            return PostCreateSerializer
        return PostSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(page=self.request.user.page_author.first())
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PostDetailView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostLikeAPIView(PostLikeView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Post.objects.all()


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


class PageFollow(APIView):
    def post(self, request, page_id):
        page = get_object_or_404(Page, pk=page_id)
        user = request.user
        page.followers.add(user)
        page.save()
        return Response({'message': 'successful '}, status=status.HTTP_200_OK)


class PageUnfollow(APIView):
    def post(self, request, page_id):
        page = get_object_or_404(Page, pk=page_id)
        user = request.user
        page.followers.remove(user)
        page.save()
        return Response({'message': 'successful '}, status=status.HTTP_200_OK)


class SearchView(ListAPIView):
    filter_backends = (filters.SearchFilter,)
    search_backends = ('title', 'page__name', 'body', 'position__name', 'category__name')
    queryset = Post.objects.all()
    serializer_class = PostSerializer
