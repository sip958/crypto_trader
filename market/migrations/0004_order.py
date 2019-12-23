# Generated by Django 2.2.8 on 2019-12-23 06:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0006_auto_20191223_0540'),
        ('market', '0003_delete_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence', models.CharField(max_length=256)),
                ('order_id', models.CharField(max_length=256)),
                ('side', models.CharField(choices=[('BUY', 'BUY'), ('SELL', 'SELL')], max_length=128)),
                ('trade_time', models.DateTimeField()),
                ('price', models.DecimalField(decimal_places=20, max_digits=40)),
                ('amount', models.DecimalField(decimal_places=20, max_digits=40)),
                ('exchange', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exchange.Exchange')),
                ('symbol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exchange.Symbol')),
            ],
        ),
    ]