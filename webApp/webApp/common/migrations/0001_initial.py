# Generated by Django 5.1.4 on 2025-02-17 06:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1000)),
                ('date_time_of_publication', models.DateTimeField(auto_now_add=True)),
                ('to_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_comments', to='blog.post')),
            ],
            options={
                'ordering': ['-date_time_of_publication'],
            },
        ),
    ]
