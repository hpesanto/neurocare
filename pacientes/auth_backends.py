"""
Backend de autenticação customizado para NeuroCare.
Autentica usuários da tabela tb_usuario.
"""

import hashlib
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from .models import Usuario


class UsuarioBackend(BaseBackend):
    """
    Autentica usando a tabela tb_usuario customizada.
    Suporta múltiplos algoritmos de hash.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Autentica usuário verificando credenciais em tb_usuario.
        
        Args:
            request: HttpRequest
            username: Login do usuário
            password: Senha em texto plano
            
        Returns:
            User object se autenticado, None caso contrário
        """
        if not username or not password:
            return None
        
        try:
            # Busca usuário na tabela tb_usuario
            usuario = Usuario.objects.get(login=username, ativo=True)
        except Usuario.DoesNotExist:
            return None
        
        # Verifica senha com múltiplos algoritmos
        if self._check_password(password, usuario.senha_hash):
            # Cria ou atualiza usuário Django correspondente
            django_user = self._get_or_create_django_user(usuario)
            return django_user
        
        return None
    
    def _check_password(self, password, stored_hash):
        """
        Verifica se a senha corresponde ao hash armazenado.
        Tenta múltiplos algoritmos (prioritiza Django hash).
        """
        # Hash Django (PRIORITÁRIO - mais seguro)
        if stored_hash.startswith('pbkdf2_') or stored_hash.startswith('argon2') or stored_hash.startswith('bcrypt'):
            return check_password(password, stored_hash)
        
        # Texto plano (inseguro, mas suportado temporariamente)
        if password == stored_hash:
            return True
        
        # MD5
        md5_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
        if md5_hash == stored_hash or md5_hash.upper() == stored_hash:
            return True
        
        # SHA256
        sha256_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if sha256_hash == stored_hash or sha256_hash.upper() == stored_hash:
            return True
        
        # SHA1
        sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest()
        if sha1_hash == stored_hash or sha1_hash.upper() == stored_hash:
            return True
        
        return False
    
    def _get_or_create_django_user(self, usuario):
        """
        Cria ou atualiza usuário Django baseado no Usuario customizado.
        """
        # Separa nome em first_name e last_name
        nome_parts = usuario.nome_completo.split() if usuario.nome_completo else ['']
        first_name = nome_parts[0] if nome_parts else ''
        last_name = ' '.join(nome_parts[1:]) if len(nome_parts) > 1 else ''
        
        # Cria ou atualiza usuário Django
        django_user, created = User.objects.get_or_create(
            username=usuario.login,
            defaults={
                'email': usuario.email,
                'first_name': first_name,
                'last_name': last_name,
                'is_active': usuario.ativo,
                'is_staff': False,
                'is_superuser': False,
            }
        )
        
        # Atualiza informações se usuário já existia
        if not created:
            django_user.email = usuario.email
            django_user.first_name = first_name
            django_user.last_name = last_name
            django_user.is_active = usuario.ativo
            django_user.save()
        
        return django_user
    
    def get_user(self, user_id):
        """
        Retorna usuário Django pelo ID.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
