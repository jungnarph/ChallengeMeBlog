# Generated by Django 5.1.5 on 2025-02-14 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0002_recipe_delete_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='instructions',
            field=models.TextField(help_text='Separate steps with a new line.'),
        ),
    ]
