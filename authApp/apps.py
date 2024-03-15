from django.apps import AppConfig


class AuthappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "authApp"

    #def ready(self):
        # Importa y registra las señales cuando la aplicación se inicie
    # import authApp.signals
