from __future__ import unicode_literals

from django.apps import AppConfig


class DataloaderinterfaceConfig(AppConfig):
    name = 'dataloaderinterface'

    def ready(self):
        import dataloaderinterface.signals