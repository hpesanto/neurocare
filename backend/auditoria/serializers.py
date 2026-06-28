from rest_framework import serializers
from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = [
            'id',
            'data_hora',
            'usuario_login',
            'perfil',
            'acao',
            'entidade',
            'objeto_id',
            'objeto_repr',
            'alteracoes',
            'ip',
            'user_agent',
            'metodo_http',
            'caminho',
        ]
        read_only_fields = fields
