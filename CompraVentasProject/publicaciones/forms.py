from django import forms
from .models import Publicacion


class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ["titulo", "descripcion", "imagen", "categorias"]

        labels = {
            "titulo": "Título",
            "descripcion": "Descripción",
            "imagen": "Imagen",
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
            "categorias": forms.CheckboxSelectMultiple()
        }
