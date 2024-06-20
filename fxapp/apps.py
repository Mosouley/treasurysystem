from django.apps import AppConfig


class FxappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fxapp'

    def ready(self):
        import fxapp.signals
