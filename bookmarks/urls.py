from django.urls import path

from bookmarks.views import BookmarkCreateAPIView, BookmarkDeleteAPIView, BookmarkListAPIView

app_name = 'bookmarks'

urlpatterns = [
    path('', BookmarkListAPIView.as_view(), name='bookmarks-list'),
    path('create/', BookmarkCreateAPIView.as_view(), name='bookmark-create'),
    path('<int:pk>/', BookmarkDeleteAPIView.as_view(), name='bookmark-delete'),
]