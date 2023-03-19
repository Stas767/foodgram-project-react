from rest_framework import mixins, viewsets


class ListCreateDestroyViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    '''Кастомный вьюсет для подписок.'''

    pass
