from django.contrib import admin
from django.urls import path
from peliculas import views  # Importa todas las vistas de la aplicación
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.catalogo, name='catalogo'),
    path('agregar/', views.agregar_pelicula, name='agregar_pelicula'),
    path('editar/<int:pk>/', views.editar_pelicula, name='editar_pelicula'),  # Ruta para editar
    path('eliminar/<int:pk>/', views.eliminar_pelicula, name='eliminar_pelicula'),  # Ruta para eliminar
    path('buscar/', views.buscar_peliculas, name='buscar_peliculas'),
    path('cargar_excel/', views.cargar_excel, name='cargar_excel'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('activate/<uuid:token>/', views.activate_account, name='activate'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('panel_usuario/', views.panel_usuario, name='panel_usuario'),
    path('', views.home, name='home'),  # Definir la vista principal
] 

# Aquí agregamos las rutas estáticas de los archivos MEDIA
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
