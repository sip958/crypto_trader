# Generated by Django 2.2.8 on 2019-12-23 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0006_order_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='sequence',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]