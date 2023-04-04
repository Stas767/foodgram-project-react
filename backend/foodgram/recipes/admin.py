from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientRecipe, Recipe, ShoppingCart, Subscription,
                     Tag)


# class RecipeIngredientsInlineAdmin(admin.TabularInline):
#     model = Recipe.ingredients.through
#     min_num = 1
#     extra = 0

#     def get_formset(self, request, obj=None, **kwargs):
#         formset = super().get_formset(request, obj=None, **kwargs)
#         formset.validate_min = True
#         return formset


# class RecipeIngredientsAdmin(admin.ModelAdmin):
#     inlines = [RecipeIngredientsInlineAdmin]


# admin.site.register(Tag)
# admin.site.register(Ingredient)
# admin.site.register(Recipe, RecipeIngredientsAdmin)
# admin.site.register(Subscription)
# admin.site.register(Favorite)
# admin.site.register(ShoppingCart)

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
    model = IngredientRecipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ('favorites', )
    list_display = ('name', 'author', )
    list_filter = ('author', 'tags', )
    search_fields = ('name', )
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
