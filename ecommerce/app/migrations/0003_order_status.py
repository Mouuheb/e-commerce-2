# Generated by Django 5.1 on 2024-08-22 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_cart_user_alter_cartitem_cart_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(default='Processing', max_length=255),
        ),
    ]
