# Generated by Django 4.1.7 on 2023-11-10 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0005_blingaccount'),
    ]

    operations = [
        migrations.AddField(
            model_name='blingaccount',
            name='token',
            field=models.CharField(blank=True, max_length=65, null=True),
        ),
        migrations.AddField(
            model_name='blingaccount',
            name='token_refresh',
            field=models.CharField(blank=True, max_length=65, null=True),
        ),
        migrations.AddField(
            model_name='blingaccount',
            name='token_vality',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
