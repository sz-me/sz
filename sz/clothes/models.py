# -*- coding: utf-8 -*-
from django.db import models
from sz.clothes.db import LowerCaseCharField

class Tag(models.Model):
    name = LowerCaseCharField(verbose_name="тэг", help_text="Без '#'", max_length=64, unique=True, db_index=True)
    def __unicode__(self):
        return u"#%s" % self.name

class Pattern(models.Model):
    tag = models.ForeignKey(Tag)
    value = LowerCaseCharField(verbose_name="несклоняемая часть", max_length=32)
    def __unicode__(self):
        return u"%s..." % self.value