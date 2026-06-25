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

    class Meta:
        model = Profissional
        fields = [
            "id", "id_perfil_acesso", "perfil_acesso_nome", "nome", "email",
            "login", "ativo", "data_criacao", "data_atualizacao",
        ]
        read_only_fields = ["id", "data_criacao", "data_atualizacao"]
        extra_kwargs = {"senha_hash": {"write_only": True, "required": False}}
