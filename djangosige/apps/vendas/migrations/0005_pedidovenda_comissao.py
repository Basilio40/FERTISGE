# Generated by Django 4.1.7 on 2023-09-05 23:53

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendas', '0004_grouppedidovenda_pedidovenda_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidovenda',
            name='comissao',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.00')), django.core.validators.MaxValueValidator(Decimal('100.00'))]),
        ),
    ]
