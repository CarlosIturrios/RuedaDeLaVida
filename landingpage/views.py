# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import TemplateView


class Index(TemplateView):
    """ landingpaga.Index
    Index view of the site
    """
    template_name = 'landingpage/index.html'
