from django.contrib import admin
from .models import Pelicula
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Profile

admin.site.register(Pelicula)


# Registrar el Usuario personalizado
class CustomUserAdmin(UserAdmin):
    model = Usuario
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']  # Opcional, agrega lo que desees ver en el listado
    list_filter = ('is_staff', 'is_superuser')  # Opcional, agrega filtros para la búsqueda
    search_fields = ['username', 'email']  # Campo para hacer búsquedas más efectivas
    
    # Si tienes campos adicionales, también puedes configurarlos como filtros, campos de búsqueda, etc.
    ordering = ['username']

admin.site.register(Usuario, CustomUserAdmin)  # Registrar el Usuario

# Registrar el modelo Profile
admin.site.register(Profile)

# Register your models here.
