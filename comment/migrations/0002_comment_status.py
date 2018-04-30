# Generated by Django 2.0.4 on 2018-04-30 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, '正常'), (2, '删除')], default=1, verbose_name='状态'),
        ),
    ]