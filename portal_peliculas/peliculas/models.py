from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Modelo de Película
class Pelicula(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    portada = models.ImageField(upload_to='portadas/')  # Se asume que se usará un sistema de carga de medios.
    trailer_url = models.URLField()
    fecha_estreno = models.DateField(null=True, blank=True)  # Campo opcional, puede estar vacío

    def __str__(self):
        return self.titulo

# Modelo de Usuario personalizado
class Usuario(AbstractUser):
    email = models.EmailField(unique=True)  # El email debe ser único

    def __str__(self):
        return self.username  # Esto asegura que el objeto Usuario sea representado por el nombre de usuario

# Modelo de Profile relacionado con Usuario
class Profile(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)  # Se establece la relación uno a uno con Usuario
    activation_token = models.UUIDField(default=uuid.uuid4, unique=True)  # Token de activación único
    is_active = models.BooleanField(default=False)  # Por defecto no está activado
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)  # Campo opcional para avatar

    def __str__(self):
        return self.user.username  # Representación del perfil por nombre de usuario

# Modelo de Serie
class Serie(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    portada = models.ImageField(upload_to='portadas_series/')  # Ruta de carga para portadas de series
    video_url = models.URLField()  # URL para ver la serie en Drive

    def __str__(self):
        return self.titulo