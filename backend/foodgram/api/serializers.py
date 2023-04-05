from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_base64.fields import Base64ImageField
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Subscription, Tag)
from rest_framework import serializers

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    '''Кастомная модель создания польз-ля.'''

    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class CustomUserSerializer(UserSerializer):
    '''Кастомная модель польз-ля.'''

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        '''Проверка на подписку.'''

        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=user, author=obj
        ).select_related().exists()


class IngredientSerializer(serializers.ModelSerializer):
    '''Ингридиенты.'''

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    '''Сериализатор для связанной моедли IngredientRecipe.'''

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), source='ingredient.id'
    )
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class FavoriteSerializer(serializers.ModelSerializer):
    '''Избранное.'''

    id = serializers.IntegerField(source='recipe.id')
    name = serializers.CharField(source='recipe.name')
    image = Base64ImageField(source='recipe.image')
    cooking_time = serializers.IntegerField(source='recipe.cooking_time')

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingCartSerializer(FavoriteSerializer):
    '''Список покупок.'''

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'cooking_time')


class TagSerializer(serializers.ModelSerializer):
    '''Теги.'''

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class PreviewRecipeSerializer(serializers.ModelSerializer):
    '''Превью рецептов.'''

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeSerializer(PreviewRecipeSerializer):
    '''Полное описание рецептов.'''

    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientRecipeSerializer(source='recipes', many=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time'
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['tags'] = TagSerializer(instance.tags, many=True).data
        return data

    def create(self, validated_data):

        tags = validated_data.pop('tags')
        recipes = validated_data.pop('recipes')

        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)

        for value in recipes:
            ingredient = value.get('ingredient')['id']
            amount = value.get('amount')
            IngredientRecipe.objects.create(
                ingredient=ingredient, recipe=recipe, amount=amount)
        return recipe

    def update(self, instance, validated_data):

        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )

        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            instance.tags.set(tags)

        if 'recipes' in validated_data:
            recipes = validated_data.pop('recipes')
            for value in recipes:
                instance.ingredient = value.get('ingredient')['id']
                instance.amount = value.get('amount')
                IngredientRecipe.objects.update(
                    ingredient=instance.ingredient,
                    recipe=instance,
                    amount=instance.amount
                )
        instance.save()
        return instance

    def get_is_favorited(self, obj):
        '''Проверка - добавлен ли рецепт в избранное.'''

        user = self.context['request'].user
        if user.is_authenticated:
            return Favorite.objects.filter(
                user=user, recipe=obj
            ).select_related().exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        '''Проверка - добавлен ли рецепт в список покупок.'''

        user = self.context['request'].user
        if user.is_authenticated:
            return ShoppingCart.objects.filter(
                user=user, recipe=obj
            ).select_related().exists()
        return False


class SubscriptionSerializer(serializers.ModelSerializer):
    '''Сериализатор подписок на автора рецепта.'''

    id = serializers.IntegerField(source='author.id')
    email = serializers.EmailField(source='author.email')
    username = serializers.CharField(source='author.username')
    first_name = serializers.CharField(source='author.first_name')
    last_name = serializers.CharField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Subscription
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, obj):
        '''Проверка на подписку.'''

        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(
                user=user, author=obj.author
            ).select_related().exists()
        return False

    def get_recipes(self, obj):
        '''Превью рецептов автора, на которого подписан.'''

        request = self.context['request']
        recipes = Recipe.objects.filter(author=obj.author).select_related()
        limit = request.GET.get('recipes_limit')
        if limit:
            recipes = recipes[:int(limit)]
        return PreviewRecipeSerializer(
            recipes, many=True,
            context={'request': request}
        ).data

    def get_recipes_count(self, obj):
        '''Возвращает количество рецептов у автора, на которого подписан.'''

        return Recipe.objects.filter(
            author=obj.author
        ).select_related().count()
