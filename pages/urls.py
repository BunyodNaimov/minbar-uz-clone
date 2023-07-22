from django.urls import path

from pages.views import PageListAPIVew, PostListCreateAPIView, UninterestingPagesList, MarkPageUninterested, \
    UnmarkPageUninteresting, PostLikeAPIView

urlpatterns = [
    path('', PageListAPIVew.as_view(), name='page_list'),
    path('blocked/', UninterestingPagesList.as_view(), name='blocked-page-list'),
    path('<int:pk>/block/', MarkPageUninterested.as_view(), name='block-page'),
    path('<int:pk>/unblock/', UnmarkPageUninteresting.as_view(), name='unblocked-page'),
    path('posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('posts/<int:post_id>/like-dislike/', PostLikeAPIView.as_view(), name='post-like-dislike'),
]
