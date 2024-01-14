from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
         'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
         'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya'}

    return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Women(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик',
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255,
                             verbose_name='Название статьи')
    slug = models.SlugField(max_length=255,
                            verbose_name='Короткое название',
                            unique=True,
                            db_index=True,
                            )
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/',
                              default=None, blank=True, null=True, verbose_name='Фотография')
    content = models.TextField(verbose_name='Текст статьи',
                               blank=True)
    time_create = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Время создания'
                                       )
    time_update = models.DateTimeField(auto_now=True,
                                       verbose_name='Последнее обновление'
                                       )
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT,
                                       verbose_name='Публикация')

    objects = models.Manager()
    published = PublishedManager()

    cat = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        related_name='posts',
        verbose_name='Категория'
    )
    tags = models.ManyToManyField(
        'TagPost',
        blank=True,
        related_name='tags',
        verbose_name='Тэги'
    )

    husbund = models.OneToOneField(
        'Husbund',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='wuman',
        verbose_name='Супруг'
    )

    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        related_name='posts',
        verbose_name='Автор статьи',
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Известная женщина'
        verbose_name_plural = 'Известные женщины'

        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(translit_to_eng(self.title))
    #     super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=255,
                            db_index=True,
                            verbose_name='Название категории')
    slug = models.SlugField(max_length=255,
                            unique=True,
                            db_index=True,
                            verbose_name='Короткое название категории')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'


class TagPost(models.Model):
    tag = models.CharField(max_length=128, db_index=True, verbose_name='Тэг')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Слаг')

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

    class Meta:
        verbose_name = 'Тэги'
        verbose_name_plural = 'Тэги'


class Husbund(models.Model):
    name = models.CharField(max_length=64, verbose_name='Имя супруга')
    age = models.IntegerField(null=True, verbose_name='Возвраст')
    m_count = models.IntegerField(blank=True, default=0, verbose_name='Количество свадеб')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Супруги'
        verbose_name_plural = 'Супруги'


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model', verbose_name='Загруженые файлы')