"""
Django Admin para gestão de usuários customizados.
Permite criar/editar usuários via interface administrativa do Django.
"""

from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django import forms
import hashlib
from .models import Usuario


class UsuarioAdminForm(forms.ModelForm):
    """
    Form customizado para criar/editar usuários.
    Adiciona campo de senha visível apenas no admin.
    """
    senha = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput,
        required=False,
        help_text='Digite a nova senha. Deixe em branco para não alterar.'
    )
    
    senha_confirmacao = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput,
        required=False,
        help_text='Digite novamente para confirmar.'
    )
    
    class Meta:
        model = Usuario
        fields = [
            'nome_completo',
            'email',
            'login',
            'ativo',
        ]
    
    def clean(self):
        """Valida que as senhas coincidem."""
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        senha_confirmacao = cleaned_data.get('senha_confirmacao')
        
        # Se preencheu senha, valida confirmação
        if senha:
            if not senha_confirmacao:
                raise forms.ValidationError('Por favor, confirme a senha.')
            if senha != senha_confirmacao:
                raise forms.ValidationError('As senhas não coincidem.')
        
        return cleaned_data
    
    def save(self, commit=True):
        """Salva usuário, gerando hash da senha se fornecida."""
        usuario = super().save(commit=False)
        
        # Se nova senha foi fornecida, gera hash
        senha = self.cleaned_data.get('senha')
        if senha:
            # Usa hash Django (mais seguro)
            usuario.senha_hash = make_password(senha)
        
        if commit:
            usuario.save()
        
        return usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    """
    Interface administrativa para modelo Usuario.
    """
    form = UsuarioAdminForm
    
    list_display = [
        'login',
        'nome_completo',
        'email',
        'ativo',
        'data_criacao',
        'data_atualizacao',
    ]
    
    list_filter = [
        'ativo',
        'data_criacao',
    ]
    
    search_fields = [
        'login',
        'nome_completo',
        'email',
    ]
    
    readonly_fields = [
        'id',
        'data_criacao',
        'data_atualizacao',
    ]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': (
                'id',
                'nome_completo',
                'email',
                'login',
                'ativo',
            )
        }),
        ('Segurança', {
            'fields': (
                'senha',
                'senha_confirmacao',
            ),
            'description': 'Configure a senha do usuário. A senha será armazenada de forma segura usando hash.'
        }),
        ('Metadados', {
            'fields': (
                'data_criacao',
                'data_atualizacao',
            ),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """ID é sempre readonly, senha_hash não aparece."""
        readonly = list(self.readonly_fields)
        if obj:  # Editando
            readonly.append('login')  # Não permite mudar login após criar
        return readonly
