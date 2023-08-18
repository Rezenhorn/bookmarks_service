from django.urls import include, path
from rest_framework import routers

from . import views

app_name = "api"

router_v1 = routers.DefaultRouter()
router_v1.register(
    "bookmarks", views.BookmarkViewSet, basename="bookmarks"
)
router_v1.register(
    "collections", views.CollectionViewSet, basename="collections"
)


urlpatterns = [
    path("", include(router_v1.urls)),
]
