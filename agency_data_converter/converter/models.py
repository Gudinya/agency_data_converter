from django.core.urlresolvers import reverse
from django.db import models


class GilKvar(models.Model):
    name = models.CharField(
        verbose_name="Наименование",
        max_length=255,
        blank=False,
        null=False)
    city = models.CharField(
        verbose_name="Город",
        max_length=255,
        blank=False,
        null=False)
    street = models.CharField(
        verbose_name="Улица",
        max_length=255,
        blank=False,
        null=False)
    house = models.CharField(
        verbose_name="Дом",
        max_length=255,
        blank=False,
        null=False)
    housing = models.CharField(
        verbose_name="Корпус",
        max_length=255,
        blank=True,
        null=True)
    site = models.CharField(
        verbose_name="Адрес сайта",
        max_length=255,
        blank=True,
        null=True)
    email = models.CharField(
        verbose_name="Контактный e-mail",
        max_length=255,
        blank=True,
        null=True)
    phone = models.CharField(
        verbose_name="Контактный тел",
        max_length=255,
        blank=True,
        null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('converter:detail', args=[str(self.id)])

    def address(self):
        strhousing = 'корп.{}'.format(self.housing) if self.housing else ''
        return ', '.join([self.street, self.house, strhousing])

class Flat(models.Model):
    YES = 'Да'
    NO = 'Нет'

    gilkvar = models.ForeignKey(GilKvar, verbose_name="ЖК")
    uid = models.CharField(
        verbose_name="Уникальный идентификатор",
        max_length=255,
        blank=False,
        null=False)
    housing = models.PositiveIntegerField(
        verbose_name="Номер корпуса",
        default=0,
        blank=False,
        null=False,)
    section = models.PositiveIntegerField(
        verbose_name="Номер секции",
        default=0,
        blank=False,
        null=False,)
    floor = models.PositiveIntegerField(
        verbose_name="Номер этажа",
        default=0,
        blank=False,
        null=False)
    num_on_floor = models.PositiveIntegerField(
        verbose_name="Номер на этаже",
        default=0,
        blank=False,
        null=False,)
    area = models.DecimalField(
        verbose_name="Площадь",
        default=0,
        max_digits=15,
        decimal_places=2,
        blank=False,
        null=False,)
    price = models.PositiveIntegerField(
        verbose_name="Цена",
        default=0,
        blank=False,
        null=False,)
    balcony = models.CharField(
        verbose_name="Балкон",
        default=NO,
        choices=((YES, 'Да'), (NO, 'Нет')),
        max_length=3,
        blank=False,
        null=False,)

    def get_absolute_url(self):
        return reverse('converter:detail_flat', args=[str(self.id)])

    class Meta:
        unique_together = ('uid', 'gilkvar',)
