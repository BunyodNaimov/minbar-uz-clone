from rest_framework import generics, permissions, status
from rest_framework.response import Response

from bookmarks.models import Bookmark
from bookmarks.serializers import BookmarkSerializer, BookmarkGetSerializer
from pages.models import Post


class BookmarkCreateAPIView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BookmarkGetSerializer

    def post(self, request, *args, **kwargs):
        post_id = request.data.get('post')
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response({'error': 'Bookmark already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': 'Bookmark created successfully.'}, status=status.HTTP_201_CREATED)


class BookmarkListAPIView(generics.ListAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)


class BookmarkDeleteAPIView(generics.RetrieveDestroyAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkGetSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        queryset = self.get_queryset()
        post_id = self.kwargs.get('pk')

        obj = generics.get_object_or_404(queryset, user=self.request.user, id=post_id)
        return obj

    def delete(self, request, *args, **kwargs):
        post_id = self.kwargs.get('pk')
        try:
            bookmark = Bookmark.objects.get(user=request.user, post_id=post_id)
        except Bookmark.DoesNotExist:
            return Response({'error': 'Bookmark does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        bookmark.delete()
        return Response({'success': 'Bookmark deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
