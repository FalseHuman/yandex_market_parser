from django.db import models
from django.contrib.auth.models import User

class TokenReset(models.Model):
    token_for_user = models.ForeignKey(
        User, related_name='token', on_delete=models.CASCADE)
    token = models.CharField(max_length=255, verbose_name="Token")

class GroupLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_group', verbose_name='Пользователь группы')
    group_name = models.CharField(max_length=10000, verbose_name='Название группы')
    

class Link(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_link', verbose_name='Пользователь ссылки')
    group_link = models.ForeignKey(GroupLink, on_delete=models.CASCADE, related_name='user_link', verbose_name='Группа')
    link = models.CharField(max_length=10000, verbose_name='Ссылка')
    name = models.CharField(max_length=10000, verbose_name='Название товара')
    def __str__(self):
        return self.link

class PriceLink(models.Model):
    price_link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name='price_link')
    price = models.CharField(max_length=10000, verbose_name='Цена')
    data_parser_price = models.DateTimeField(auto_now_add=True, verbose_name='Дата парсинга цены')
    def __str__(self):
        return self.price

class AnalogLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_analog_link', verbose_name='Пользователь аналоговой ссылки')
    analog_link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name='analog_link')
    link = models.CharField(max_length=10000, verbose_name='Ссылка')
    analog_name = models.CharField(max_length=10000, verbose_name='Название товара')
    def __str__(self):
        return self.link

class AnalogLinkPrice(models.Model):
    analog_link_price = models.ForeignKey(AnalogLink, on_delete=models.CASCADE, related_name='analog_link_price')
    analog_price = models.CharField(max_length=10000, verbose_name='Цена')
    analog_data_parser_price = models.DateTimeField(auto_now_add=True, verbose_name='Дата парсинга цены')

    def __str__(self):
        return self.analog_price