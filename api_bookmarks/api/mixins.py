from rest_framework import mixins, viewsets


class ListRetrieveCreateDeleteViewSet(mixins.CreateModelMixin,
                                      mixins.DestroyModelMixin,
                                      mixins.ListModelMixin,
                                      mixins.RetrieveModelMixin,
                                      viewsets.GenericViewSet):
    pass
