# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class EneagramaConfig(AppConfig):
    name = 'Eneagrama'

    def ready(self):
        super(EneagramaConfig, self).ready()
