# Generated by Django 2.0.5 on 2018-05-07 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0004_auto_20180507_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sidebar',
            name='display_type',
            field=models.PositiveIntegerField(choices=[(1, 'HTML'), (2, '最新文章'), (3, '最热文章'), (4, '最近评论'), (5, '友链')], default=1, verbose_name='展示类型'),
        ),
    ]