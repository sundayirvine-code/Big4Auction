# Generated by Django 5.0.1 on 2024-01-25 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction_app', '0005_user_stripe_customer_id_alter_user_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=150, null=True, unique=True),
        ),
    ]
