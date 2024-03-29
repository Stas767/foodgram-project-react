import django_filters
from recipes.models import Ingredient, Recipe, Tag
from rest_framework.filters import SearchFilter


class SearchIngredient(SearchFilter):
    search_param = 'name'

    class Meta:
        model = Ingredient
        fields = ('name', )


class RecipeFilter(django_filters.FilterSet):
    '''Фильтрация по вложенным полям в модели Recipe.'''

    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = django_filters.NumberFilter(
        method='filter_is_favorited',
    )
    is_in_shopping_cart = django_filters.NumberFilter(
        method='filter_is_in_shopping_cart',
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart', )

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(shopping_carts__user=self.request.user)
        return queryset
