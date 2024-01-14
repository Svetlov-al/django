# Generated by Django 4.2.1 on 2024-01-13 15:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='Название категории')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Короткое название категории')),
            ],
            options={
                'verbose_name': 'Категории',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Husbund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Имя супруга')),
                ('age', models.IntegerField(null=True, verbose_name='Возвраст')),
                ('m_count', models.IntegerField(blank=True, default=0, verbose_name='Количество свадеб')),
            ],
            options={
                'verbose_name': 'Супруги',
                'verbose_name_plural': 'Супруги',
            },
        ),
        migrations.CreateModel(
            name='TagPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(db_index=True, max_length=128, verbose_name='Тэг')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Тэги',
                'verbose_name_plural': 'Тэги',
            },
        ),
        migrations.CreateModel(
            name='UploadFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads_model', verbose_name='Загруженые файлы')),
            ],
        ),
        migrations.CreateModel(
            name='Women',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название статьи')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Короткое название')),
                ('photo', models.ImageField(blank=True, default=None, null=True, upload_to='photos/%Y/%m/%d/', verbose_name='Фотография')),
                ('content', models.TextField(blank=True, verbose_name='Текст статьи')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')),
                ('is_published', models.BooleanField(choices=[(False, 'Черновик'), (True, 'Опубликовано')], default=0, verbose_name='Публикация')),
                ('author', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='Автор статьи')),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='women.category', verbose_name='Категория')),
                ('husbund', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wuman', to='women.husbund', verbose_name='Супруг')),
                ('tags', models.ManyToManyField(blank=True, related_name='tags', to='women.tagpost', verbose_name='Тэги')),
            ],
            options={
                'verbose_name': 'Известная женщина',
                'verbose_name_plural': 'Известные женщины',
                'ordering': ['-time_create'],
                'indexes': [models.Index(fields=['-time_create'], name='women_women_time_cr_9f33c2_idx')],
            },
        ),
    ]
