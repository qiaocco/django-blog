# Generated by Django 2.2.6 on 2019-10-20 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveIntegerField(choices=[(0, '删除'), (1, '正常'), (2, '草稿')], default=1, verbose_name='状态')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=64, verbose_name='名称')),
                ('is_nav', models.BooleanField(default=0, verbose_name='是否置顶导航')),
            ],
            options={
                'verbose_name': '分类',
                'verbose_name_plural': '分类',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveIntegerField(choices=[(0, '删除'), (1, '正常'), (2, '草稿')], default=1, verbose_name='状态')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=64, verbose_name='名称')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveIntegerField(choices=[(0, '删除'), (1, '正常'), (2, '草稿')], default=1, verbose_name='状态')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('title', models.CharField(max_length=255, verbose_name='标题')),
                ('content', models.TextField(help_text='正文仅支持Markdown语法', verbose_name='正文')),
                ('html', models.TextField(default='', help_text='正文仅支持Markdown语法', verbose_name='渲染后的内容')),
                ('is_markdown', models.BooleanField(default=True, verbose_name='使用Markdown格式')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Slug')),
                ('desc', models.CharField(blank=True, max_length=1024, verbose_name='摘要')),
                ('pv', models.PositiveIntegerField(default=0, verbose_name='pv')),
                ('uv', models.PositiveIntegerField(default=0, verbose_name='uv')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blog.Category', verbose_name='分类')),
                ('tag', models.ManyToManyField(to='blog.Tag', verbose_name='标签')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
                'ordering': ('-id',),
            },
        ),
    ]
