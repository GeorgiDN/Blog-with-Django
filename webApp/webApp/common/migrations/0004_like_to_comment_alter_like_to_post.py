# Generated by Django 5.1.4 on 2025-01-04 09:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_image'),
        ('common', '0003_alter_comment_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='to_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_likes', to='common.comment'),
        ),
        migrations.AlterField(
            model_name='like',
            name='to_post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_likes', to='blog.post'),
        ),
    ]
