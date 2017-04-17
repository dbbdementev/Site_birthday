from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class User_info(models.Model):
    surname = models.CharField(max_length=30, blank=True)
    name = models.CharField(max_length=30, blank=True)
    middlename = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=30, blank=True)
    phone = models.BigIntegerField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(null=True, max_length=5, blank=True)
    time_zone = models.CharField(max_length=30, blank=True)
    time_congratulations = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return "%s %s " % (self.surname, self.name)


class Common(models.Model):
    id_email = models.CharField(max_length=30, null=True, blank=True)
    id_vk = models.CharField(max_length=30, null=True, blank=True)
    id_ok = models.CharField(max_length=30, null=True, blank=True)
    id_f = models.CharField(max_length=30, null=True, blank=True)


class Register_vk(models.Model):
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    nickname = models.CharField(max_length=30, null=True, blank=True)
    data_visit = models.DateTimeField(null=True, blank=True)
    auth_id = models.OneToOneField(User)


class Register_ok(models.Model):
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    nickname = models.CharField(max_length=30, null=True, blank=True)
    data_visit = models.DateField(null=True, blank=True)


class Type(models.Model):
    country = models.CharField(max_length=30, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    data = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Congratulations(models.Model):
    type_id = models.ForeignKey(Type, null=True, blank=True)
    user_id = models.ForeignKey(User_info, null=True, blank=True)
    status = models.PositiveSmallIntegerField(help_text="2-одобрено, 1-на проверке, 0-отказано", null=True, blank=True)
    category_cmc = models.CharField(max_length=30, null=True, blank=True)
    text = models.CharField(max_length=300, null=True, blank=True)
    data_created = models.DateTimeField(null=True, blank=True)


class Letters(models.Model):
    user_letters = models.ForeignKey(User_info, verbose_name="Отправитель", null=True, blank=True)
    text_letters = models.CharField(verbose_name="Текст", max_length=300, null=True, blank=True)
    date_create = models.DateTimeField(verbose_name="Дата отправки", null=True, blank=True)
    email_create = models.EmailField(verbose_name="Почта отправителя", null=True, blank=True)
    date_send = models.DateTimeField(verbose_name="Дата получения", null=True, blank=True)
    email_send = models.EmailField(verbose_name="Почта получателя", null=True, blank=True)
    status = models.CharField(max_length=5, verbose_name="Статус отправки письма",
                              help_text="2-одобрено, 1-на проверке, 0-отказано", null=True, blank=True)

    # is_hotified=models.EmailField(verbose_name="Уведомление",help_text="2-уведомлен, 1-не уведомлен, 0-не уведомлять",null=True, blank=True)

    def __str__(self):
        return "%s %s " % (self.text_letters, self.date_send)
