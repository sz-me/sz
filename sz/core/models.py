# -*- coding: utf-8 -*-
from django.db import models
from sz.core.db import LowerCaseCharField
from django.contrib import auth
from sz.core.algorithms import stemmers

class Category(models.Model):
    name = LowerCaseCharField(
        verbose_name=u"категория",
        help_text=u"Например, часть тела, для которой предназначена вещь",
        max_length=64,
        primary_key=True,
        db_index=True)
    def __unicode__(self):
        return u"%s" % self.name
    class Meta:
        verbose_name = u"категория"
        verbose_name_plural = u"категории"

class Thing(models.Model):
    tag = LowerCaseCharField(
        verbose_name=u"тэг",
        help_text=u"Без '#'",
        max_length=64,
        primary_key=True,
        db_index=True)
    stem = LowerCaseCharField(
        verbose_name=u"основа",
        help_text=u"Основа слова для поиска",
        max_length=64,
        unique=True,
        db_index=True,
        editable=False)
    category = models.ForeignKey(
        Category,
        verbose_name=u"категория")
    def save(self, *args, **kwargs):
        stemmer = stemmers.RussianStemmer()
        self.stem = stemmer.stemWord(self.tag)
        super(Thing, self).save(*args, **kwargs)
    def __unicode__(self):
        return u"#%s" % self.tag
    class Meta:
        verbose_name = u"вещь"
        verbose_name_plural = u"вещи"

class Message(models.Model):
    text = models.TextField(max_length=1024, verbose_name=u"сообщение") #Like a TEXT field
    latitude = models.FloatField(verbose_name=u"широта")
    longitude = models.FloatField(verbose_name=u"долгота")
    accuracy = models.FloatField(verbose_name=u"точность")
    city_id = models.IntegerField(
        verbose_name=u"Идентификатор в GeoNames",
        db_index=True,
        null=False,
        blank=False)
    place_id = models.CharField(
        max_length=24,
        verbose_name=u"Идентификатор в Foursquare",
        db_index=True,
        null=False,
        blank=False)
    bargain_date = models.DateTimeField(
        verbose_name=u"дата покупки",
        null=True,
        blank=True)
    date = models.DateTimeField(
        auto_now_add=True,
        null=False,
        editable=False,
        verbose_name=u"дата добавления")
    things = models.ManyToManyField(
        Thing,
        null=True,
        blank=True)
    user = models.ForeignKey(
        auth.models.User,
        verbose_name=u"пользователь")
    class Meta:
        verbose_name = u"сообщение"
        verbose_name_plural = u"сообщения"
    def __unicode__(self):
        return self.text
