from django.db import models
from users.models import User
from ingredients.models import Ingredient, IngredientRecipe
from tags.models import Tag, TagRecipe


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Картинка рецепта'
    )
    text = models.TextField('Описание рецепта')
    ingredients = models.ManyToManyField(
        Ingredient,
        through=IngredientRecipe,
        through_fields=('ingredient', 'recipe'),
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        through=TagRecipe,
        through_fields=('tag', 'recipe'),
        verbose_name='Теги'
    )
    cooking_time = models.PositiveIntegerField('Время приготовления в минутах')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        ordering = [('-pub_date')]
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
