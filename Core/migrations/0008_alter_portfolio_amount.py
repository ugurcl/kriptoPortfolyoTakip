# Generated by Django 5.2 on 2025-05-01 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0007_alter_portfolio_amount_alter_portfolio_buy_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='amount',
            field=models.DecimalField(decimal_places=1, max_digits=20),
        ),
    ]
