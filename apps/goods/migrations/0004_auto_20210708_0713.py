# Generated by Django 2.2.5 on 2021-07-08 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_remove_sku_caption'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sku',
            name='name',
            field=models.CharField(max_length=200, verbose_name='名称'),
        ),
    ]