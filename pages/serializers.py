from rest_framework import serializers

from pages.models import Page


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = (
            'id', 'name', 'slug', 'picture', 'author', 'is_organization', 'followers_count', 'followed'
        )
        read_only_fields = ('id', 'picture', 'followers_count', 'followed')
