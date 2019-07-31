from django.apps import AppConfig


class StrathideasappConfig(AppConfig):
    name = 'strathideasapp'

    def ready(self):
        import strathideasapp.signals

