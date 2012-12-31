# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from sz.core.db import LowerCaseCharField
from django.contrib import auth
from sz.core.morphology import stemmers

class Category(models.Model):
    name = LowerCaseCharField(
        verbose_name=u"наименование",
        max_length=64,
        primary_key=True,
        db_index=True)
    BODY_PART_CHOICES = (
        ('head', 'Head'),
        ('top', 'Top'),
        ('palms', 'Palms'),
        ('bottom', 'Bottom'),
        ('feed', 'Feed'),
    )
    body_part = models.CharField(
        max_length=8,
        choices=BODY_PART_CHOICES,
        verbose_name=u"часть тела",
    )
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('kid', 'Kid'),
    )
    gender = models.CharField(
        max_length=8,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
        verbose_name=u"пол",
    )
    LAYER_CHOICES = (
        ('under', 'Under'),
        ('middle', 'Middle'),
        ('outer', 'Outer'),
        )
    layer = models.CharField(
        max_length=8,
        choices=LAYER_CHOICES,
        verbose_name=u"слой",
    )
    def __unicode__(self):
        return u"%s" % self.name
    class Meta:
        verbose_name = u"категория"
        verbose_name_plural = u"категории"

class Thing(models.Model):
    name = LowerCaseCharField(
        verbose_name=u"наименование",
        help_text=u"Определяет принадлежность сообщения к категории",
        max_length=64,
        primary_key=True,
        db_index=True)
    stem = LowerCaseCharField(
        verbose_name=u"основа",
        help_text=u"Строка, проверяемая на вхождение",
        max_length=64,
        unique=True,
        db_index=True,
        editable=False)
    category = models.ForeignKey(
        Category,
        verbose_name=u"категория")
    def save(self, *args, **kwargs):
        stemmer = stemmers.RussianStemmer()
        self.stem = stemmer.stemWord(self.name)
        super(Thing, self).save(*args, **kwargs)
    def __unicode__(self):
        return u"%s" % self.name
    class Meta:
        verbose_name = u"вещь"
        verbose_name_plural = u"вещи"

class Place(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=24,
        verbose_name=u"идентификатор в Foursquare")
    name = models.CharField(max_length=128, verbose_name=u"название")
    address = models.CharField(max_length=128, verbose_name=u"адрес",
        null=True,
        blank=True,)
    crossStreet = models.CharField(max_length=128, verbose_name=u"пересечение улиц",
        null=True,
        blank=True,)
    contact = models.CharField(max_length=512, verbose_name=u"контакты")
    position = models.PointField(verbose_name=u"координаты")
    def longitude(self):
        return self.position.x
    def latitude(self):
        return self.position.y
    city_id = models.IntegerField(
        verbose_name=u"идентификатор в GeoNames",
        db_index=True,
        null=False,
        blank=False)
    date = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name=u"дата синхронизации")
    objects = models.GeoManager()
    def foursquare_details_url(self):
        return "https://foursquare.com/v/%s" % self.id
    foursquare_icon_prefix = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name=u"префикс пиктограммы категории в Foursquare")
    foursquare_icon_suffix = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        verbose_name=u"суффикс (расширение) пиктограммы категории в Foursquare")
    def __unicode__(self):
        return u"%s" % self.name + (self.address and (u", %s" % self.address) or u"")
    class Meta:
        verbose_name = u"место"
        verbose_name_plural = u"места"
        ordering = ["name"]

class Message(models.Model):
    date = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
        editable=False,
        verbose_name=u"дата добавления")
    text = models.TextField(
        max_length=1024,
        null=False,
        blank=False,
        verbose_name=u"сообщение")
    user = models.ForeignKey(
        auth.models.User,
        verbose_name=u"пользователь")
    place = models.ForeignKey(
        Place,
        verbose_name=u"место")
    things = models.ManyToManyField(
        Thing,
        null=True,
        blank=True)
    class Meta:
        verbose_name = u"сообщение"
        verbose_name_plural = u"сообщения"
        ordering = ["-date"]
    def __unicode__(self):
        return u"%s" % self.text
