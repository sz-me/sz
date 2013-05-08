# -*- coding: utf-8 -*-
import os
import uuid
import time

from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.gis.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from imagekit import models as imagekit_models
from imagekit import processors
from south.modelsinspector import add_introspection_rules


class ModifyingFieldDescriptor(object):
    """ Modifies a field when set using the field's (overriden) .to_python() method. """

    def __init__(self, field):
        self.field = field

    def __get__(self, instance, owner=None):
        if instance is None:
            raise AttributeError('Can only be accessed via an instance.')
        return instance.__dict__[self.field.name]

    def __set__(self, instance, value):
        instance.__dict__[self.field.name] = self.field.to_python(value)


class LowerCaseCharField(models.CharField):
    def to_python(self, value):
        value = super(LowerCaseCharField, self).to_python(value)
        if isinstance(value, basestring):
            return value.lower()
        return value

    def contribute_to_class(self, cls, name):
        super(LowerCaseCharField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, ModifyingFieldDescriptor(self))


add_introspection_rules([], ["^sz\.core\.models\.LowerCaseCharField"])


# Entities
LANGUAGE_CHOICES = (
    ('en', _('English')),
    ('ru', _('Russian')),
)


class Category(models.Model):

    alias = models.SlugField(
        verbose_name=u"псевдоним", max_length=32,
        db_index=True, unique=True)

    name = models.CharField(verbose_name=u"наименование", max_length=64, db_index=True)

    description = models.CharField(
        verbose_name=u"описание", max_length=256,
        null=True, blank=True)

    keywords = models.TextField(
        verbose_name=u"ключевые слова", max_length=2048,
        help_text=u"ключевые слова, разделённые запятыми, регистр неважен")

    def get_keywords_list(self):
        normalized_keywords = u' '.join(self.keywords.split()).lower()
        return sorted([kw.strip() for kw in normalized_keywords.split(',')])

    def save(self, *args, **kwargs):
        self.keywords = u', '.join(self.get_keywords_list())
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        verbose_name = u"категория"
        verbose_name_plural = u"категории"


class Place(models.Model):

    id = models.CharField(primary_key=True, max_length=24, verbose_name=u"идентификатор в Foursquare")

    name = models.CharField(max_length=128, verbose_name=u"название")

    address = models.CharField(max_length=128, verbose_name=u"адрес", null=True, blank=True, )

    crossStreet = models.CharField(max_length=128, verbose_name=u"пересечение улиц", null=True, blank=True, )

    contact = models.CharField(max_length=512, verbose_name=u"контакты")

    position = models.PointField(verbose_name=u"координаты")

    def longitude(self):
        return self.position.x

    def latitude(self):
        return self.position.y

    city_id = models.IntegerField(
        verbose_name=u"идентификатор в GeoNames", db_index=True,
        null=False, blank=False)

    date = models.DateTimeField(
        auto_now=True, editable=False,
        verbose_name=u"дата синхронизации")

    objects = models.GeoManager()

    def foursquare_details_url(self):
        return "https://foursquare.com/v/%s" % self.id

    foursquare_icon_prefix = models.CharField(
        max_length=128, null=True, blank=True,
        verbose_name=u"префикс пиктограммы категории в Foursquare")
    foursquare_icon_suffix = models.CharField(
        max_length=16, null=True, blank=True,
        verbose_name=u"суффикс (расширение) пиктограммы категории в Foursquare")

    def __unicode__(self):
        return u"%s" % self.name + (self.address and (u", %s" % self.address) or u"")

    class Meta:
        verbose_name = u"место"
        verbose_name_plural = u"места"
        ordering = ("name",)


class Stem(models.Model):

    stem = LowerCaseCharField(
        verbose_name=u"основа слова", max_length=32,
        db_index=True, unique=True)

    language = LowerCaseCharField(
        verbose_name=u"язык", db_index=True, max_length=2,
        choices=LANGUAGE_CHOICES)

    def __unicode__(self):
        return u"%s" % self.stem

    class Meta:
        unique_together = ('stem', 'language',)


class Style(models.Model):
    name = models.CharField(max_length=32, verbose_name=_('name'))
    description = models.CharField(
        verbose_name=_('description'), max_length=256,
        null=True, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        verbose_name = _('style')
        verbose_name_plural = _('styles')


EMOTION_CHOICES = (
    ('smile', 'Smile'),
    ('lol', "LOL"),
    ('bad', 'Bad'),
    ('indifferent', 'Indifferent')
)


class UserManager(BaseUserManager):
    def _create_user(self, email, password):
        now = timezone.now()
        user = self.model(
            email=UserManager.normalize_email(email),
            is_active=True, is_superuser=False,
            last_login=now, date_joined=now
        )
        user.set_password(password)
        return user

    def create_user(self, email, style, password=None):
        if not style:
            raise ValueError('Users must select a style')

        if not email:
            raise ValueError('Users must have an email address')

        user = self._create_user(email, password)
        user.style = style
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self._create_user(email, password)
        user.is_superuser = True
        user.save(using=self._db)
        return user


GENDER_CHOICES = (
    ('M', _('male')),
    ('F', _('female')),
)


class User(AbstractBaseUser):
    email = models.CharField(
        _('email address'), max_length=72, unique=True,
        db_index=True, validators=[validators.EmailValidator()]
    )
    style = models.ForeignKey(
        Style, verbose_name=_('style'),
        blank=True, null=True
    )
    date_of_birth = models.DateField(
        _('birthday'), blank=True, null=True
    )
    gender = models.CharField(
        _('gender'), max_length=1, blank=True,
        null=True, choices=GENDER_CHOICES
    )
    is_superuser = models.BooleanField(
        _('superuser status'), default=False,
        help_text=_('Designates that this user has all permissions without '
                    'explicitly assigning them.'))
    is_active = models.BooleanField(
        _('active'), default=True,
        help_text=_(
            'Designates whether this user should be treated as '
            'active. Unselect this instead of deleting accounts.'
        )
    )
    date_joined = models.DateTimeField(
        _('date joined'), default=timezone.now
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_superuser

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class Smile(models.Model):
    emotion = models.CharField(
        max_length=16, verbose_name=_('emotion'),
        choices=EMOTION_CHOICES
    )
    style = models.ForeignKey(Style, verbose_name=u"стиль", blank=True, null=True)

    def __unicode__(self):
        style_name = self.style and self.style.name or 'all'
        return u"%s_%s" % (self.emotion, style_name)

    class Meta:
        verbose_name = u"смайл"
        verbose_name_plural = u"смайлы"


class MessageBase(models.Model):

    date = models.DateTimeField(
        auto_now_add=True, null=True, blank=True,
        editable=False, verbose_name=u"дата добавления")

    text = models.TextField(
        max_length=1024, null=False,
        blank=True, verbose_name=u"сообщение")

    user = models.ForeignKey(User, verbose_name=_('user'))

    place = models.ForeignKey(Place, verbose_name=u"место")

    def get_photo_path(self, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        directory = time.strftime('photos/%Y/%m/%d')
        return os.path.join(directory, filename)

    photo = imagekit_models.ProcessedImageField(
        upload_to=get_photo_path, verbose_name=u"фотография", null=False, blank=True,
        processors=[processors.ResizeToFit(1350, 1200), ], options={'quality': 85}
    )

    reduced_photo = imagekit_models.ImageSpecField(
        [processors.ResizeToFit(435, 375), ],
        image_field='photo', options={'quality': 85})

    thumbnail = imagekit_models.ImageSpecField(
        [processors.ResizeToFill(90, 90), ],
        image_field='photo', options={'quality': 85})

    def get_photo_absolute_urls(self, photo_host_url=""):
        photo_host_url = photo_host_url.rstrip('/')
        if self.photo:
            return dict(full=photo_host_url + self.photo.url, reduced=photo_host_url + self.reduced_photo.url,
                        thumbnail=photo_host_url + self.thumbnail.url)
        else:
            return None

    categories = models.ManyToManyField(Category, null=True, blank=True)

    smile = models.ForeignKey(Smile)

    class Meta:
        abstract = True
        verbose_name = u"сообщение"
        verbose_name_plural = u"сообщения"

    def __unicode__(self):
        return u"%s" % self.text

    def save(self, force_insert=False, force_update=False, using=None):
        if self.text is None:
            self.text = ''
        self.text = self.text.strip()
        models.Model.save(self, force_insert=force_insert, force_update=force_update, using=using)


class Message(MessageBase):
    stems = models.ManyToManyField(Stem, null=True, blank=True)


class MessagePreview(MessageBase):
    pass


class CensorBox(models.Model):

    message_preview = models.ForeignKey(MessagePreview)

    x = models.FloatField()
    y = models.FloatField()
    r = models.FloatField()


