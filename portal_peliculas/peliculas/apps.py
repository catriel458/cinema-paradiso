from django.apps import AppConfig

class PeliculasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'peliculas'

    def ready(self):
        import peliculas.signals  # Asegúrate de importar signals

