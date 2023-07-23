from rest_framework import serializers

from categories.serializers import CategorySerializer
from pages.models import Page, Post, PageInteraction, Position, PostLike, Comment, CommentLike
from users.serializers import UserSerializer


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = (
            'id', 'name', 'slug', 'picture', 'author', 'is_organization', 'followers_count', 'followed'
        )
        read_only_fields = ('id', 'picture', 'followers_count', 'followed')


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True).fields.get('username')

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'post', 'likes', 'dislikes')
        read_only_fields = ('id', 'author', 'post')


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ('id', 'post', 'comment', 'value')


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('id', 'name')
        read_only_fields = ('id',)


class PostAuthorSerializer(serializers.ModelSerializer):
    position = PositionSerializer(read_only=True, many=True)

    class Meta:
        model = Page
        fields = ('id', 'name', 'position')
        read_only_fields = ('id',)


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ('id', 'post', 'value')


class PostSerializer(serializers.ModelSerializer):
    author = PostAuthorSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    categories = CategorySerializer(read_only=True, many=True)
    likes = serializers.IntegerField(read_only=True)
    dislikes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = (
            'id', 'title', 'slug', 'image', 'description', 'views', 'visible', 'allow_comments', 'publish_date',
            'likes', 'dislikes', 'categories', 'author', 'comments')
        read_only_fields = ('id',)


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'description', 'image', 'author', 'views', 'visible')
        read_only_fields = ('id',)


class BlockedPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageInteraction
        fields = ('id', 'user', 'page')
        read_only_fields = ('id',)
