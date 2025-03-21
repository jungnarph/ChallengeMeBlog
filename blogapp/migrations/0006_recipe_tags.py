# Generated by Django 5.1.5 on 2025-03-21 14:42

import taggit.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0005_comment'),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
