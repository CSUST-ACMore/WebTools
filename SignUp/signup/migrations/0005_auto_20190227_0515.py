# Generated by Django 2.1.7 on 2019-02-27 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0004_auto_20190224_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='bronze_num',
            field=models.IntegerField(default=16, verbose_name='铜奖数量'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='gold_num',
            field=models.IntegerField(default=6, verbose_name='金奖数量'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='silver_num',
            field=models.IntegerField(default=10, verbose_name='银奖数量'),
        ),
    ]
