from django import forms
from django.contrib.auth.models import User
from .models import Publicacion


class RegistroForm(forms.Form):
    """Formulario de registro de usuario.

    Campos: nombre, apellido, correo electrónico, contraseña y confirmación.
    Utiliza el modelo User de Django para almacenar los usuarios registrados.
    """

    first_name = forms.CharField(
        max_length=30,
        label="Nombre",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ej: María",
        }),
    )
    last_name = forms.CharField(
        max_length=30,
        label="Apellido",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ej: González",
        }),
    )
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "correo@ejemplo.com",
        }),
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Mínimo 8 caracteres",
        }),
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Repite tu contraseña",
        }),
    )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Ya existe una cuenta registrada con este correo electrónico."
            )
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        if p1 and len(p1) < 8:
            self.add_error(
                "password1",
                "La contraseña debe tener al menos 8 caracteres.",
            )

        return cleaned_data

    def save(self):
        """Crea y retorna un nuevo usuario con los datos del formulario."""
        data = self.cleaned_data
        user = User.objects.create_user(
            username=data["email"],
            email=data["email"],
            password=data["password1"],
            first_name=data["first_name"],
            last_name=data["last_name"],
        )
        return user


class LoginForm(forms.Form):
    """Formulario de inicio de sesión.

    Valida el correo electrónico y la contraseña del usuario.
    """

    username = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "correo@ejemplo.com",
        }),
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Tu contraseña",
        }),
    )


class PublicacionForm(forms.ModelForm):
    
    nueva_categoria = forms.CharField(required=False, label="Nueva categoría")
    def clean_nueva_categoria(self):
        categoria = self.cleaned_data["nueva_categoria"].strip()
        return categoria  


    class Meta:
        model = Publicacion
        fields = ["titulo", "descripcion", "imagen","precio","ubicacion","disponibilidad","nombre_vendedor",
                  "correo_electronico","telefono", "categorias"]

        labels = {
            "titulo": "Título",
            "descripcion": "Descripción",
            "imagen": "Imagen",
            "precio": "Precio",
            "ubicacion": "Ubicación",
            "disponibilidad": "Disponibilidad",
            "nombre_vendedor": "Nombre del vendedor",
            "correo_electronico": "Correo electrónico",
            "telefono": "Teléfono",
            "categorias": "Categorías",
        }

        widgets = {
            "titulo": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej: Alfajor artesanal"
            }),
            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Describe el producto, precio, estado, forma de entrega, etc."
            }),
            "imagen": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "precio": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Ej: 5000"
            }),

            "ubicacion": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej: Beauchef 850"
            }),

            "disponibilidad": forms.Select(attrs={
                "class": "form-control"
            }),

            "nombre_vendedor": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nombre completo"
            }),

            "correo_electronico": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "correo@ejemplo.com"
            }),

            "telefono": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "+56 9 1234 5678"
            }),          
            "categorias": forms.CheckboxSelectMultiple()
        }
    def clean_titulo(self):
        titulo = self.cleaned_data["titulo"].strip()
        if len(titulo)< 3:
            raise forms.ValidationError("El título debe tener al menos 3 caracteres.")
        return titulo
    
    def clean(self):
        cleaned_data = super().clean()
        categorias = cleaned_data.get("categorias")
        nueva_categoria=cleaned_data.get("nueva_categoria", "").strip()

        if not categorias and not nueva_categoria:
            raise forms.ValidationError("Debe seleccionar o crear al menos una categoría.")
        return cleaned_data