from django.db.utils import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from bookmarks.models import Bookmark, Collection
from .services import parse_tags


class BookmarkSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    link = serializers.URLField()

    class Meta:
        model = Bookmark
        fields = '__all__'
        read_only_fields = (
            'author',
            'title',
            'description',
            'type',
            'image',
            'created_at',
            'updated_at',
            'collections'
        )

    def create(self, validated_data):
        try:
            data = parse_tags(validated_data['link'])
            return Bookmark.objects.create(
                **data,
                author=self.context['request'].user,
                link=validated_data['link']
            )
        except IntegrityError:
            raise ValidationError(
                {'detail': 'Данная ссылка уже в закладках.'}
            )


class CollectionSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Collection
        fields = ('author', 'title', 'description', 'bookmarks')
        read_only_fields = ('author', 'bookmarks')

    def create(self, validated_data):
        return Collection.objects.create(
            **validated_data,
            author=self.context['request'].user,
        )
