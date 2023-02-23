from django.contrib import admin

from .models import Tag, Ingredient, Recipe


class RecipeIngredientsInlineAdmin(admin.TabularInline):
    model = Recipe.ingredients.through
    min_num = 1
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj=None, **kwargs)
        formset.validate_min = True
        return formset


class RecipeIngredientsAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientsInlineAdmin]


admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeIngredientsAdmin)
