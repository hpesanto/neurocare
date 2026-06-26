import hashlib

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import PerfilAcesso, Profissional


class PerfilAcessoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilAcesso
        fields = ["id", "nome", "descricao", "data_criacao", "data_atualizacao"]
        read_only_fields = ["id", "data_criacao", "data_atualizacao"]


class ProfissionalSerializer(serializers.ModelSerializer):
    perfil_acesso_nome = serializers.CharField(
        source="id_perfil_acesso.nome", read_only=True, default=None
    )
    senha = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Profissional
        fields = [
            "id", "id_perfil_acesso", "perfil_acesso_nome", "nome", "email",
            "login", "senha", "ativo", "data_criacao", "data_atualizacao",
        ]
        read_only_fields = ["id", "data_criacao", "data_atualizacao"]

    def create(self, validated_data):
        senha = validated_data.pop("senha", "changeme")
        validated_data["senha_hash"] = hashlib.sha256(senha.encode()).hexdigest()
        prof = super().create(validated_data)
        self._sync_django_user(prof, senha)
        return prof

    def update(self, instance, validated_data):
        senha = validated_data.pop("senha", None)
        if senha:
            validated_data["senha_hash"] = hashlib.sha256(senha.encode()).hexdigest()
        prof = super().update(instance, validated_data)
        if senha:
            self._sync_django_user(prof, senha)
        return prof

    def _sync_django_user(self, prof, senha):
        nome_parts = prof.nome.split() if prof.nome else [""]
        first_name = nome_parts[0]
        last_name = " ".join(nome_parts[1:]) if len(nome_parts) > 1 else ""

        django_user, created = User.objects.get_or_create(
            username=prof.login,
            defaults={
                "email": prof.email,
                "first_name": first_name,
                "last_name": last_name,
            },
        )
        django_user.set_password(senha)
        django_user.email = prof.email
        django_user.first_name = first_name
        django_user.last_name = last_name
        django_user.is_active = prof.ativo
        django_user.save()
