import hashlib

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
        return super().create(validated_data)

    def update(self, instance, validated_data):
        senha = validated_data.pop("senha", None)
        if senha:
            validated_data["senha_hash"] = hashlib.sha256(senha.encode()).hexdigest()
        return super().update(instance, validated_data)
