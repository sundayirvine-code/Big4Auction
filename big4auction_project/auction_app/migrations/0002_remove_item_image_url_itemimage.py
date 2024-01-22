# Generated by Django 5.0.1 on 2024-01-22 20:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='image_url',
        ),
        migrations.CreateModel(
            name='ItemImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='auction_app.item')),
            ],
        ),
    ]
