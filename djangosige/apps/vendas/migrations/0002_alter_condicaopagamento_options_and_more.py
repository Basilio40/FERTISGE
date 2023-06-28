# Generated by Django 4.1.7 on 2023-06-02 03:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0004_alter_localestoque_options_and_more'),
        ('vendas', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='condicaopagamento',
            options={'verbose_name': 'Condição de Pagamento'},
        ),
        migrations.AlterModelOptions(
            name='orcamentovenda',
            options={'verbose_name': 'Orçamento de Venda'},
        ),
        migrations.AlterModelOptions(
            name='pedidovenda',
            options={'permissions': (('faturar_pedidovenda', 'Pode faturar Pedidos de Venda'),), 'verbose_name': 'Pedido de Venda'},
        ),
        migrations.AlterField(
            model_name='condicaopagamento',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='itensvenda',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='pagamento',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='venda',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='venda',
            name='local_orig',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='venda_local_estoque', to='estoque.localestoque'),
        ),
    ]
