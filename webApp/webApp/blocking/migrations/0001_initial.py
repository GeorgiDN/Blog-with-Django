# Generated by Django 5.1.4 on 2025-01-13 16:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('blocked', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked', to=settings.AUTH_USER_MODEL)),
                ('blocker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocking', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('blocker', 'blocked')},
            },
        ),
    ]
