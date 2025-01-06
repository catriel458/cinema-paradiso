from django import forms
from .models import Pelicula
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Usuario, Profile

class PeliculaForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = ['titulo', 'descripcion', 'portada', 'trailer_url', 'fecha_estreno']
        widgets = {
            'fecha_estreno': forms.DateInput(attrs={'type': 'date'}),  # Input tipo fecha
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Usuario  # Utiliza tu modelo 'Usuario' si estás usando un modelo personalizado.
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
            raise forms.ValidationError("La contraseña debe contener al menos 2 caracteres alfanuméricos.")
        if not any(char.isupper() for char in password):
            raise forms.ValidationError("La contraseña debe contener al menos 1 letra mayúscula.")
        return password


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2']

class AvatarUploadForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'accept': 'image/jpeg,image/png'}),
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            # Validar que sea JPG o PNG
            if avatar.content_type not in ['image/jpeg', 'image/png']:
                raise forms.ValidationError("El archivo debe ser JPG o PNG.")
        return avatar


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = Usuario
        fields = ['old_password', 'new_password1', 'new_password2']
