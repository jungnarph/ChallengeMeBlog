# Generated by Django 5.1.5 on 2025-02-14 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0003_alter_recipe_instructions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.TextField(help_text='Separate ingredients with a semicolon.'),
        ),
    ]
