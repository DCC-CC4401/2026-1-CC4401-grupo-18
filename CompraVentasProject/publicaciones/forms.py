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
    def clean_titulo(self):
        titulo = self.cleaned_data["titulo"].strip()
        if len(titulo)< 3:
            raise forms.ValidationError("El título debe tener al menos 3 caracteres.")
        return titulo
    
    def clean_categorias(self):
        categorias = self.cleaned_data.get("categorias")
        if not categorias:
            raise forms.ValidationError("Debe seleccionar al menos una categoría.")
        return categorias
