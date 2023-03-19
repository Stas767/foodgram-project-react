from django.db import IntegrityError
from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from api import serializers
from recipes.models import Ingredient, Recipe, Tag, Subscription


User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.CustomUserSerializer

    @action(detail=False, permission_classes=(IsAuthenticated, ),)
    def subscriptions(self, request):
        '''Получение списка подписок текущего пользователя.'''

        user = request.user
        queryset = Subscription.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = serializers.SubscriptionSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=('post', 'delete'))
    def subscribe(self, request, id=None):
        '''Логика подписки/отписки на конкретного пользователя.'''

        user = self.request.user
        author = self.get_object()

        if user == author:
            return Response(
                {'errors': 'Вы не можете подписаться на самого себя!'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.method == 'POST':
            try:
                subscribe = Subscription.objects.create(
                    user=user, author=author)
            except IntegrityError:
                return Response(
                    {'errors': 'Вы уже подписались на автора!'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = serializers.SubscriptionSerializer(
                subscribe, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            subscription = get_object_or_404(
                Subscription,
                user=user,
                author=author
            )
            subscription.delete()
            return Response(
                {'messsage': 'Вы отписались от автора.'},
                status=status.HTTP_204_NO_CONTENT
            )


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
