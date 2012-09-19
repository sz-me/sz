from django.db import models
from sz.core.db import LowerCaseCharField
from django.contrib import auth

class Tag(models.Model):
    name = LowerCaseCharField(verbose_name=u"тэг", help_text="Без '#'", max_length=64, unique=True, db_index=True)
    def __unicode__(self):
        return u"#%s" % self.name
    class Meta:
        verbose_name = u"тэг"
        verbose_name_plural = u"тэги"

class Pattern(models.Model):
    tag = models.ForeignKey(Tag)
    value = LowerCaseCharField(verbose_name=u"словоформа или синоним", max_length=32)
    def __unicode__(self):
        return u"%s..." % self.value
    class Meta:
        verbose_name = "словоформа"
        verbose_name_plural = "словоформы"

class Message(models.Model):
    text = models.TextField(max_length=1024) #Like a TEXT field
    begin = models.DateField(auto_now_add=True)
    end = models.DateField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    pub_date = models.DateTimeField(auto_now_add=True) #Like a DATETIME field
    user = models.ForeignKey(auth.models.User)
    def __unicode__(self): #Tell it to return as a unicode string (The name of the to-do item) rather than just Object.
        return self.text
