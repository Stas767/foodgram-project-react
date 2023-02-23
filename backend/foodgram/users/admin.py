from django.contrib import admin
from django.contrib.auth import get_user_model


User = get_user_model()


class CustomUserdmin(admin.ModelAdmin):
    '''Насройка админки для модели CustomUser.'''

    list_display = (
        'pk',
        'email',
        'username',
        'first_name',
        'last_name',
        'password'
    )
    search_fields = ('email', 'username')
    list_filter = ('email', 'username')
    empty_value_display = '-пусто-'


admin.site.register(User, CustomUserdmin)
