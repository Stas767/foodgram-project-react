# Generated by Django 2.2.16 on 2023-03-19 14:12

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0006_auto_20230227_1312'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SpoppingCart',
            new_name='ShoppingCart',
        ),
    ]
