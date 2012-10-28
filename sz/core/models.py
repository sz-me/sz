from django.db import models
from sz.core.db import LowerCaseCharField
from django.contrib import auth

class Tag(models.Model):
    name = LowerCaseCharField(verbose_name=u"тэг", help_text="Без '#'", max_length=64, unique=True, db_index=True)
    def __unicode__(self):
        return u"#%s" % self.name
    class Meta:
        abstract = True
        verbose_name = u"тэг"
        verbose_name_plural = u"тэги"

class Pattern(models.Model):
    #tag = models.ForeignKey(Tag)
    value = LowerCaseCharField(verbose_name=u"словоформа или синоним", max_length=32)
    def __unicode__(self):
        return u"%s..." % self.value
    class Meta:
        abstract = True
        verbose_name = u"словоформа"
        verbose_name_plural = u"словоформы"

class DomainTag(Tag):
    class Meta:
        verbose_name = u"тэг предметной области"
        verbose_name_plural = u"тэги предметной области"

class DomainPattern(Pattern):
    tag = models.ForeignKey(DomainTag, related_name='pattern_set')
    class Meta:
        verbose_name = u"словоформа предметной области"
        verbose_name_plural = u"словоформы предметной области"
"""
class Place(models.Model):
    id = models.CharField(primary_key=True, max_length=24, db_index=True)
    name = models.CharField(verbose_name=u"Название", max_length=64)
    address = models.CharField(verbose_name=u"Адрес", max_length=256)
    latitude = models.FloatField()
    longitude = models.FloatField()
    class Meta:
        verbose_name = u"тэг положения"
        verbose_name_plural = u"тэги положения"
"""
class Message(models.Model):
    text = models.TextField(max_length=1024) #Like a TEXT field
    latitude = models.FloatField()
    longitude = models.FloatField()
    accuracy = models.FloatField()
    bargain_date = models.DateTimeField()
    pub_date = models.DateTimeField(auto_now_add=True) #Like a DATETIME field
    user = models.ForeignKey(auth.models.User)
    place_id = models.CharField(max_length=24, db_index=True)
    def __unicode__(self): #Tell it to return as a unicode string (The name of the to-do item) rather than just Object.
        return self.text
