from django import forms
from .models import Publicacion


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