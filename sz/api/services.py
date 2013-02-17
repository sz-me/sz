# -*- coding: utf-8 -*-
from django.core import paginator as django_paginator
from sz import settings
from sz.core import models, utils, gis
from sz.core.gis import geonames, venue
from sz.core.morphology.tagging import *

def paginated_content(queryset, page=None, paginate_by=5):
    paginator = django_paginator.Paginator(queryset, paginate_by)
    try:
        messages = paginator.page(page)
    except django_paginator.PageNotAnInteger:
        messages = paginator.page(1)
    except django_paginator.EmptyPage:
        messages = paginator.page(paginator.num_pages)
    return messages

def tags2dict(tags):
    d = dict((tag.name, [p.value for p in tag.pattern_set.all()]) for tag in tags)
    return d

def tagging_service(message, tags, algorithm):
    tags_dict = tags2dict(tags)
    return algorithm(message, tags_dict)
    
def regexp_tagging_service(message, tags):
    algorithm = lambda m, t: regexp_tagging_algorithm(m, t)
    return tagging_service(message, tags, algorithm)

def spellcorrector_tagging_service(message, tags):
    algorithm = lambda m, t: spellcorrector_tagging_algorithm(m, t)
    return tagging_service(message, tags, algorithm)

