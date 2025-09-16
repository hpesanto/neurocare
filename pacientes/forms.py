from django import forms

from .models import Paciente


class PacienteForm(forms.ModelForm):
    # Represent genero as a simple CharField in the form (comma-separated values)
    genero = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Paciente
        fields = [
            "cpf",
            "nome",
            "rg",
            "genero",
            "estado_civil",
            "profissao",
            "tel_1",
            "tel_2",
            "email",
            "logradouro",
            "num_fachada",
            "complemento",
            "bairro",
            "municipio",
            "uf",
            "cep",
            "contato_emergencia",
            "tel_contato_emergencia",
            "parentesco_contato_emergencia",
        ]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "cpf": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If editing an instance where genero is a list, join to a comma string for the form field
        instance = getattr(self, "instance", None)
        if instance and getattr(instance, "genero", None):
            g = instance.genero
            if isinstance(g, (list, tuple)):
                self.fields["genero"].initial = ", ".join([str(x) for x in g if x])

    def clean_genero(self):
        data = self.cleaned_data.get("genero")
        if not data:
            return []
        # split by comma and strip
        parts = [p.strip() for p in data.split(",") if p.strip()]
        return parts

    def save(self, commit=True):
        # Ensure genero is stored in the correct format expected by the model (list or string)
        obj = super().save(commit=False)
        genero_val = self.cleaned_data.get("genero")
        # If the model expects a list (ArrayField), assign the list; otherwise join to string
        if hasattr(obj, "genero"):
            field = obj._meta.get_field("genero")
            if field.__class__.__name__ == "ArrayField":
                obj.genero = genero_val
            else:
                # store as comma-separated string
                obj.genero = (
                    ", ".join(genero_val)
                    if isinstance(genero_val, (list, tuple))
                    else (genero_val or "")
                )
        if commit:
            obj.save()
        return obj
