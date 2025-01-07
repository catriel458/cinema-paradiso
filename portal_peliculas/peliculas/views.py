from django.shortcuts import render, get_object_or_404, redirect
from .models import Pelicula
from .forms import PeliculaForm
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
import pandas as pd
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from .forms import RegistroForm
from .forms import SerieForm
from .forms import CustomUserCreationForm
from .models import Usuario,Profile
from django.http import HttpResponse
import uuid  # Si usas UUIDField
from django.contrib.auth import update_session_auth_hash
from .forms import AvatarUploadForm
from .forms import CustomPasswordChangeForm
from django.core.files.images import get_image_dimensions
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .models import Serie


def home(request):
    return render(request, 'catalogo.html')

def activate_account(request, token):
    try:
        profile = Profile.objects.get(activation_token=token)
        if not profile.is_active:
            profile.is_active = True
            profile.user.is_active = True
            profile.save()
            profile.user.save()
            return HttpResponse("Cuenta activada con éxito. Ahora puede iniciar sesión.")
        else:
            return HttpResponse("Este enlace ya ha sido utilizado.")
    except Profile.DoesNotExist:
        return HttpResponse("Enlace de activación inválido.")


def send_activation_email(user):
    profile = Profile.objects.get(user=user)
    activation_link = f"http://127.0.0.1:8000/activate/{profile.activation_token}"  # Cambia por tu URL de producción
    subject = "Activación de Cuenta - Cinema Paradiso"
    message = f"""
    Bienvenido a Cinema Paradiso,
    
    Gracias por registrarse en nuestra página. 
    Haga clic en el siguiente enlace para validar su cuenta:
    
    {activation_link}
    """
    send_mail(subject, message, 'catrielcabrera97@gmail.com', [user.email])

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)  # Cambia el formulario a AuthenticationForm
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('catalogo')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def registro_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Crea el usuario
            user = form.save()

            # Crear un perfil asociado al usuario
            profile = Profile.objects.create(user=user, activation_token=uuid.uuid4())

            # Establece el estado 'is_active' como False en el perfil
            profile.is_active = False
            profile.save()

            # Desactiva el usuario hasta que se active
            user.is_active = False
            user.save()

            # Enviar correo con el enlace de activación
            send_activation_email(user)

            return render(request, 'register_done.html')  # Página indicando que verifique su correo
        else:
            return render(request, 'registro.html', {'form': form, 'error': form.errors})
    else:
        form = CustomUserCreationForm()
    return render(request, 'registro.html', {'form': form})


# Vista para mostrar el catálogo de películas
def catalogo(request):
    # Obtén todas las películas ordenadas por fecha de estreno descendente
    lista_peliculas = Pelicula.objects.all().order_by('-fecha_estreno')
    
    # Configura la paginación con 6 películas por página
    paginator = Paginator(lista_peliculas, 6)
    page_number = request.GET.get('page')
    peliculas = paginator.get_page(page_number)
    
    # Renderiza la plantilla con las películas paginadas
    return render(request, 'catalogo.html', {'peliculas': peliculas})

# Vista para agregar una nueva película
def agregar_pelicula(request):
    if request.method == 'POST':
        form = PeliculaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalogo')  # Redirige al catálogo después de guardar
    else:
        form = PeliculaForm()
    return render(request, 'agregar_pelicula.html', {'form': form})

# Vista para editar una película
def editar_pelicula(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)
    if request.method == 'POST':
        form = PeliculaForm(request.POST, request.FILES, instance=pelicula)
        if form.is_valid():
            form.save()
            return redirect('catalogo')  # Redirige al catálogo después de guardar los cambios
    else:
        form = PeliculaForm(instance=pelicula)
    return render(request, 'editar_pelicula.html', {'form': form, 'pelicula': pelicula})


def eliminar_pelicula(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)
    pelicula.delete()
    return redirect('catalogo')  # Redirige al catálogo después de eliminar la película

# Vista para agregar una nueva película
def agregar_serie(request):
    if request.method == 'POST':
        form = SerieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalogo_series')  # Redirige a las series después de guardar
    else:
        form = SerieForm()  # Corregido el formulario de serie
    return render(request, 'agregar_serie.html', {'form': form})

# Vista para editar una película
def editar_serie(request, pk):
    serie = get_object_or_404(Serie, pk=pk)  # Corregido: usar `Serie` en vez de `Pelicula`
    if request.method == 'POST':
        form = SerieForm(request.POST, request.FILES, instance=serie)
        if form.is_valid():
            form.save()
            return redirect('catalogo_series')  # Redirige a las series después de guardar los cambios
    else:
        form = SerieForm(instance=serie)
    return render(request, 'editar_serie.html', {'form': form, 'serie': serie})

# Vista para eliminar una serie
def eliminar_serie(request, pk):
    serie = get_object_or_404(Serie, pk=pk)
    serie.delete()  # Corregido: cambiar `pelicula.delete()` a `serie.delete()`
    return redirect('catalogo_series')  # Redirige a las series después de eliminar la serie

# Vista para mostrar el catálogo de series
def catalogo_series(request):
    lista_series = Serie.objects.all().order_by('-titulo')  # Puedes ordenar por fecha si tienes un campo de fecha en `Serie`.
    paginator = Paginator(lista_series, 6)
    page_number = request.GET.get('page')
    series = paginator.get_page(page_number)
    return render(request, 'catalogo_series.html', {'series': series})



# Vista para buscar películas

def buscar_peliculas(request):
    query = request.GET.get('q', '')
    if query:
        peliculas = Pelicula.objects.filter(
            titulo__icontains=query
        ) | Pelicula.objects.filter(
            descripcion__icontains=query
        )
        resultados = [{
            'titulo': pelicula.titulo,
            'descripcion': pelicula.descripcion,
            'fecha_estreno': pelicula.fecha_estreno.strftime('%d %b, %Y'),
            'imagen': pelicula.portada.url if pelicula.portada else None
        } for pelicula in peliculas]
        return JsonResponse(resultados, safe=False)
    return JsonResponse([], safe=False)

# Vista para buscar series
def buscar_series(request):
    query = request.GET.get('q', '')
    if query:
        series = Serie.objects.filter(
            titulo__icontains=query
        ) | Serie.objects.filter(
            descripcion__icontains=query
        )
        resultados = [{
            'titulo': serie.titulo,
            'descripcion': serie.descripcion,
            'imagen': serie.portada.url if serie.portada else None  # Corregido
        } for serie in series]
        return JsonResponse(resultados, safe=False)
    return JsonResponse([], safe=False)

# Vista para cargar el archivo Excel y agregar las películas
# Vista para cargar películas desde Excel
def cargar_excel(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)
        filepath = fs.url(filename)

        # Leer el archivo Excel usando pandas
        df = pd.read_excel(filepath)

        # Asumimos que las columnas del Excel son: 'titulo', 'descripcion', 'fecha_estreno', 'portada_url'
        for index, row in df.iterrows():
            Pelicula.objects.create(
                titulo=row['titulo'],
                descripcion=row['descripcion'],
                fecha_estreno=row['fecha_estreno'],
                portada_url=row['portada_url']
            )

        # Responder con un mensaje de éxito
        return JsonResponse({"message": "Películas cargadas exitosamente"}, status=200)

    return JsonResponse({"message": "Error al cargar el archivo"}, status=400)

# Vista para el panel de usuario:

@login_required
def panel_usuario(request):
    user = request.user
    profile = user.profile  # Accede al perfil del usuario

    avatar_form = AvatarUploadForm(instance=profile)  # Formulario para el avatar
    password_form = PasswordChangeForm(user)  # Formulario para la contraseña

    if request.method == 'POST':
        if 'update_avatar' in request.POST:  # Si el usuario presiona el botón de actualizar avatar
            avatar_form = AvatarUploadForm(request.POST, request.FILES, instance=profile)
            if avatar_form.is_valid():
                avatar_form.save()  # Guarda la nueva imagen
                messages.success(request, "Avatar actualizado con éxito.")
            else:
                messages.error(request, "Hubo un error al cargar el avatar.")
        
        elif 'update_password' in request.POST:  # Si el usuario presiona el botón de actualizar contraseña
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                password_form.save()  # Guarda la nueva contraseña
                update_session_auth_hash(request, password_form.user)  # Evita que el usuario se desloguee
                messages.success(request, "Contraseña actualizada con éxito.")
            else:
                messages.error(request, "Hubo un error al cambiar la contraseña.")

    return render(request, 'panel_usuario.html', {
        'avatar_form': avatar_form,
        'password_form': password_form,
        'user': user,
        'profile': profile
    })
