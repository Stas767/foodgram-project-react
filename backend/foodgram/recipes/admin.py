from django.contrib import admin
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Subscription, Tag)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):

    list_display = ('user', 'recipe', )
    list_filter = ('user', )
    search_fields = ('recipe__name', )
    search_help_text = 'Название рецепта'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):

    list_display = ('name', 'measurement_unit', )
    list_filter = ('measurement_unit', )
    search_fields = ('name', )
    search_help_text = 'NAME'
    list_per_page = 50


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    list_display = ('slug', )
    search_fields = ('slug', )
    search_help_text = 'SLUG тега'


class IngredientRecipeAdminInline(admin.TabularInline):
    '''Инлайн для связанной модели IngredientRecipe.'''

    model = IngredientRecipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):

    readonly_fields = ('favorites', )
    list_display = ('name', 'author', 'favorites')
    list_filter = ('author', 'tags', )
    search_fields = ('name', 'tags__name')
    search_help_text = 'NAME'
    list_per_page = 50
    inlines = [IngredientRecipeAdminInline, ]

    def favorites(self, obj):
        return obj.favorites.count()


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):

    list_display = ('user', 'recipe', )
    list_filter = ('user', )
    search_fields = ('recipe__name', )
    search_help_text = 'Название рецепта'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):

    list_display = ('user', 'author', )
    list_filter = ('user', 'author', )
