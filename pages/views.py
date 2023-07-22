from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.generics import ListAPIView, ListCreateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pages.models import Page, Post, PageInteraction, PostLike
from pages.serializers import PageSerializer, PostSerializer, BlockedPageSerializer, PostCreateSerializer, \
    PostLikeSerializer


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


class PostLikeDislikeAPIView(CreateAPIView):
    serializer_class = PostLikeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            post_id = serializer.validated_data['post'].id
            value = serializer.validated_data['value']
            try:
                like = PostLike.objects.get(user=user, post_id=post_id)
                if like.value == 1:
                    # Если пользователь нажал на кнопку лайка дважды, то мы отменяем свой голос
                    like.post.likes -= 1
                    like.value = 0
                    like.post.save()
                    like.delete()
                else:
                    # Если пользователь изменил свой голос, то мы сначала снимаем старый голос
                    like.post.likes -= 1
                    # Затем добавляем новый голос
                    like.value = 1
                    like.post.save()
                    like.save()
            except PostLike.DoesNotExist:
                serializer.save(user=user)
                post = serializer.validated_data['post']
                if value == 1:
                    post.likes += 1
                else:
                    post.dislikes += 1
                post.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


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
