from django.urls import path

from bookmarks.views import BookmarkCreateAPIView, BookmarkDeleteAPIView

app_name = 'bookmarks'

urlpatterns = [
    path('', BookmarkCreateAPIView.as_view(), name='bookmarks-create'),
    path('<int:pk>/', BookmarkDeleteAPIView.as_view(), name='bookmarks-delete'),
]