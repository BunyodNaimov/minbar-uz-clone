from django.urls import path

from pages.views import PageListAPIVew, PostListCreateAPIView, UninterestingPagesList, MarkPageUninterested, \
    UnmarkPageUninteresting, CommentListCreateAPIView, PostLikeAPIView, CommentLikeAPIView, PageFollow, PageUnfollow, \
    PageDetailView, PostDetailView

urlpatterns = [

    path('', PageListAPIVew.as_view(), name='page_list'),
    path('<int:pk>/', PageDetailView.as_view(), name='page_detail'),
    path('blocked/', UninterestingPagesList.as_view(), name='blocked-page-list'),
    path('<int:page_id>/follow/', PageFollow.as_view(), name='page_follow'),
    path('<int:page_id>/unfollow/', PageUnfollow.as_view(), name='page_unfollow'),
    path('posts/<int:pk>/block/', MarkPageUninterested.as_view(), name='block-page'),
    path('posts/<int:pk>/unblock/', UnmarkPageUninteresting.as_view(), name='unblocked-page'),
    path('posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/detail_update/', PostDetailView.as_view(), name='post-detail-update'),
    path('posts/<int:pk>/like-dislike/', PostLikeAPIView.as_view(), name='post_like'),
    path('posts/<int:post_id>/comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('<int:post_id>/comments/<int:comment_id>/', CommentLikeAPIView.as_view(), name='comment_like'),
]
