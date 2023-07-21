from django.urls import path

from bookmark.views import BookmarkCreateAPIView, BookmarkDeleteAPIView

app_name = 'bookmarks'

urlpatterns = [
    path('', BookmarkCreateAPIView.as_view(), name='bookmark-create'),
    path('<int:pk>/', BookmarkDeleteAPIView.as_view(), name='bookmark-delete'),
]