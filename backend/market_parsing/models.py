from tkinter.tix import Tree
from django.db import models
from django.contrib.auth.models import User

class TokenReset(models.Model):
    token_for_user = models.ForeignKey(
        User, related_name='token', on_delete=models.CASCADE)
    token = models.CharField(max_length=255, verbose_name="Token")

class Link(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_link', verbose_name='Пользователь')
    link = models.CharField(max_length=10000, verbose_name='Ссылка')
    comment = models.TextField( null=True, blank=True, verbose_name='Комментарий к ссылке')
    #email_send = models.BooleanField(null=True, blank=True, default="False", verbose_name='Уведомлять об изменении цены')
    def __str__(self):
        return self.link

class PriceLink(models.Model):
    price_link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name='price_link')
    price = models.CharField(max_length=10000, verbose_name='Цена')
    data_parser_price = models.DateTimeField(auto_now_add=True, verbose_name='Дата парсинга цены')
    def __str__(self):
        return self.price