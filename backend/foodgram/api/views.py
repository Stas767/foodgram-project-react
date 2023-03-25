import csv

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api import serializers
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Subscription, Tag)

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

    @action(detail=True, methods=('post', 'delete'))
    def favorite(self, request, pk=None):
        '''Логика добавления/удаления рецепта в избранное.'''

        user = self.request.user
        recipe = self.get_object()

        if request.method == 'POST':
            try:
                favorite = Favorite.objects.create(
                    user=user, recipe=recipe)
            except IntegrityError:
                return Response(
                    {'errors': 'Этот рецепт уже добавлен в избранное!'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = serializers.FavoriteShoppingCartSerializer(
                favorite, context={'request': request}
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        if request.method == 'DELETE':
            favorite = get_object_or_404(
                Favorite,
                user=user,
                recipe=recipe
            )
            favorite.delete()
            return Response(
                {'messsage': 'Рецепт успешно удален из избранного.'},
                status=status.HTTP_204_NO_CONTENT
            )

    @action(detail=True, methods=('post', 'delete'))
    def shopping_cart(self, request, pk=None):
        '''Логика добавления/удаления рецепта в список покупок.'''

        user = self.request.user
        recipe = self.get_object()

        if request.method == 'POST':
            try:
                shopping_cart = ShoppingCart.objects.create(
                    user=user, recipe=recipe)
            except IntegrityError:
                return Response(
                    {'errors': 'Этот рецепт уже добавлен в список покупок!'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = serializers.FavoriteShoppingCartSerializer(
                shopping_cart, context={'request': request}
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        if request.method == 'DELETE':
            favorite = get_object_or_404(
                ShoppingCart,
                user=user,
                recipe=recipe
            )
            favorite.delete()
            return Response(
                {'messsage': 'Рецепт успешно удален из списка покупок.'},
                status=status.HTTP_204_NO_CONTENT
            )

    @action(detail=False)
    def download_shopping_cart(self, request):
        '''Загрузить список покупок в pdf.'''

        ingredients = (
            IngredientRecipe.objects
            .filter(recipe__shopping_carts__user=request.user)
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(amount=Sum('amount'))
            .order_by()
        )

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="shop_list.csv"'
        writer = csv.writer(response)
        writer.writerow(['Список покупок:'])
        writer.writerow([' '])  # добавить пустую строку
        for ingredient in ingredients:
            name = ingredient['ingredient__name']
            measurement_unit = ingredient['ingredient__measurement_unit']
            amount = ingredient['amount']
            writer.writerow([f'{name} - {amount} {measurement_unit}'])
        return response


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
