from django import forms
from django.contrib.auth.hashers import make_password

from profissionais.models import Profissional


class UsuarioForm(forms.ModelForm):
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=False,
        label="Senha",
    )

    class Meta:
        model = Profissional
        fields = [
            "id_perfil_acesso",
            "nome",
            "email",
            "login",
            "senha",
            "ativo",
        ]
        widgets = {
            "id_perfil_acesso": forms.Select(attrs={"class": "form-control"}),
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "login": forms.TextInput(attrs={"class": "form-control"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = Profissional.objects.filter(email=email)
        if self.instance and getattr(self.instance, "pk", None):
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Já existe um usuário com este e-mail.")
        return email

    def clean_login(self):
        login = self.cleaned_data.get("login")
        qs = Profissional.objects.filter(login=login)
        if self.instance and getattr(self.instance, "pk", None):
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Login já está em uso.")
        return login

    def save(self, commit=True):
        instance = super().save(commit=False)
        senha = self.cleaned_data.get("senha")
        # Only set senha_hash if a password was provided
        if senha:
            instance.senha_hash = make_password(senha)
        if commit:
            instance.save()
        return instance
