from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from bookmarks.models import Bookmark, Collection
from .mixins import ListRetrieveCreateDeleteViewSet
from .serializers import BookmarkSerializer, CollectionSerializer

User = get_user_model()


class BookmarkViewSet(ListRetrieveCreateDeleteViewSet):
    serializer_class = BookmarkSerializer

    def get_queryset(self):
        return Bookmark.objects.filter(author=self.request.user)

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='collection/(?P<collection_pk>[^/.]+)'
    )
    def collection(self, request, pk, collection_pk):
        bookmark = get_object_or_404(Bookmark, pk=pk)
        collection = get_object_or_404(Collection, pk=collection_pk)
        serializer = CollectionSerializer(collection)
        collection_bookmark = bookmark.collections.filter(pk=collection_pk)
        if request.method == "DELETE" and collection_bookmark.exists():
            bookmark.collections.remove(collection)
            return Response(status=status.HTTP_204_NO_CONTENT)
        if request.method == "POST" and not collection_bookmark.exists():
            bookmark.collections.add(collection)
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(
            data={"error": (f"This bookmark is already "
                            f"in collection <{collection.title}>")},
            status=status.HTTP_400_BAD_REQUEST
        )


class CollectionViewSet(ModelViewSet):
    serializer_class = CollectionSerializer

    def get_queryset(self):
        return Collection.objects.filter(author=self.request.user)
