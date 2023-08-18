from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Bookmark(models.Model):
    class LinkType(models.TextChoices):
        WEBSITE = "website", _("website")
        BOOK = "book", _("book")
        ARTICLE = "article", _("article")
        MUSIC = "music", _("music")
        VIDEO = "video", _("video")

    link = models.TextField(verbose_name='Ссылка', unique=True)
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        related_name="bookmarks"
    )
    title = models.TextField(verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    type = models.CharField(
        verbose_name='Тип ссылки',
        max_length=7,
        choices=LinkType.choices,
        default=LinkType.WEBSITE,
    )
    image = models.TextField(verbose_name='Превью картинки')
    created_at = models.DateTimeField(
        verbose_name='Дата и время создания', auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Дата и время редактирования', auto_now=True
    )
    collections = models.ManyToManyField(
        to='Collection', verbose_name='Коллекция', related_name='bookmarks'
    )

    class Meta:
        verbose_name = 'Закладка страницы'
        verbose_name_plural = 'Закладки страниц'

    def __str__(self):
        return f"Закладка <{self.link}>"


class Collection(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        related_name="collections"
    )
    title = models.TextField(verbose_name='Название', unique=True)
    description = models.TextField(verbose_name='Описание')
    created_at = models.DateTimeField(
        verbose_name='Дата и время создания', auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Дата и время редактирования', auto_now=True
    )

    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'

    def __str__(self):
        return f"Коллекция {self.title}"
