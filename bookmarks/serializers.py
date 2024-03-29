from rest_framework import serializers

from bookmarks.models import Bookmark
from pages.serializers import PostSerializer


class BookmarkSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True).fields.get('title')

    class Meta:
        model = Bookmark
        fields = ('id', 'post')


class BookmarkCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bookmark
        fields = ('id', 'post')

