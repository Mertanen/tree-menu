from django.db import models
from django.utils.translation import gettext_lazy as _


class Menu(models.Model):
    ''' Модель меню '''
    title = models.CharField(verbose_name=_('Название'), max_length=255, unique=True)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = _('Меню')
        verbose_name_plural = _('Меню')
        ordering = ['title', ]

class MenuItem(models.Model):
    ''' Модель элементов меню '''
    menu = models.ForeignKey(
        Menu,
        verbose_name=_('Меню'),
        on_delete=models.CASCADE,
        blank=True,
        related_name='items',
    )

    parent = models.ForeignKey(
        'self',
        verbose_name=_('Родитель'),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children',
    )
    title = models.CharField(verbose_name=_('Название'), max_length=255)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = _('Элемент меню')
        verbose_name_plural = _('Элементы меню')
        ordering = ['menu', 'title', ]