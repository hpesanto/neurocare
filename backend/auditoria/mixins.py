from rest_framework import serializers
from .utils import (
    get_client_ip,
    get_user_agent,
    remove_sensitive_fields,
    compute_diff,
)
from .services import registrar_log


class AuditLogMixin:
    """
    Mixin para capturar CREATE, UPDATE, DELETE e LEITURA (retrieve) em ViewSets.
    Registra automaticamente em AuditLog de forma best-effort.
    """

    def get_audit_info(self):
        """Extrair informações básicas de request para auditoria."""
        request = self.request
        user = request.user

        return {
            'ip': get_client_ip(request),
            'user_agent': get_user_agent(request),
            'metodo_http': request.method,
            'caminho': request.path,
            'id_usuario': user.id if user.is_authenticated else None,
            'usuario_login': user.username if user.is_authenticated else 'anônimo',
        }

    def get_profissional_info(self):
        """Extrair id_profissional e perfil do usuário autenticado."""
        request = self.request
        user = request.user

        id_profissional = None
        perfil = None

        if user.is_authenticated:
            try:
                from profissionais.models import Profissional
                prof = Profissional.objects.get(usuario=user)
                id_profissional = prof.id
                perfil = prof.tipo_profissional or 'N/A'
            except Exception:
                pass

        return id_profissional, perfil

    def get_object_repr(self, instance):
        """Extrair representação legível do objeto."""
        try:
            return str(instance)
        except Exception:
            return f"{instance.__class__.__name__}"

    def serialize_instance(self, instance):
        """Serializar instância removendo campos sensíveis."""
        if hasattr(self, 'get_serializer'):
            ser = self.get_serializer(instance)
            data = ser.data if hasattr(ser, 'data') else {}
        else:
            data = {}

        return remove_sensitive_fields(data)

    def perform_create(self, serializer):
        """Capturar CREATE."""
        super().perform_create(serializer)
        instance = serializer.instance

        audit_info = self.get_audit_info()
        id_profissional, perfil = self.get_profissional_info()
        alteracoes = self.serialize_instance(instance)

        registrar_log(
            usuario_login=audit_info['usuario_login'],
            acao='CREATE',
            entidade=instance.__class__.__name__,
            objeto_id=str(instance.pk),
            objeto_repr=self.get_object_repr(instance),
            alteracoes=alteracoes,
            id_usuario=audit_info['id_usuario'],
            id_profissional=id_profissional,
            perfil=perfil,
            ip=audit_info['ip'],
            user_agent=audit_info['user_agent'],
            metodo_http=audit_info['metodo_http'],
            caminho=audit_info['caminho'],
        )

    def perform_update(self, serializer):
        """Capturar UPDATE com diff."""
        instance = self.get_object()
        old_data = self.serialize_instance(instance)

        super().perform_update(serializer)

        new_data = self.serialize_instance(instance)
        alteracoes = compute_diff(old_data, new_data)

        audit_info = self.get_audit_info()
        id_profissional, perfil = self.get_profissional_info()

        registrar_log(
            usuario_login=audit_info['usuario_login'],
            acao='UPDATE',
            entidade=instance.__class__.__name__,
            objeto_id=str(instance.pk),
            objeto_repr=self.get_object_repr(instance),
            alteracoes=alteracoes,
            id_usuario=audit_info['id_usuario'],
            id_profissional=id_profissional,
            perfil=perfil,
            ip=audit_info['ip'],
            user_agent=audit_info['user_agent'],
            metodo_http=audit_info['metodo_http'],
            caminho=audit_info['caminho'],
        )

    def perform_destroy(self, instance):
        """Capturar DELETE."""
        audit_info = self.get_audit_info()
        id_profissional, perfil = self.get_profissional_info()

        registrar_log(
            usuario_login=audit_info['usuario_login'],
            acao='DELETE',
            entidade=instance.__class__.__name__,
            objeto_id=str(instance.pk),
            objeto_repr=self.get_object_repr(instance),
            alteracoes=None,
            id_usuario=audit_info['id_usuario'],
            id_profissional=id_profissional,
            perfil=perfil,
            ip=audit_info['ip'],
            user_agent=audit_info['user_agent'],
            metodo_http=audit_info['metodo_http'],
            caminho=audit_info['caminho'],
        )

        super().perform_destroy(instance)

    def retrieve(self, request, *args, **kwargs):
        """Capturar LEITURA (retrieve)."""
        instance = self.get_object()

        audit_info = self.get_audit_info()
        id_profissional, perfil = self.get_profissional_info()

        registrar_log(
            usuario_login=audit_info['usuario_login'],
            acao='LEITURA',
            entidade=instance.__class__.__name__,
            objeto_id=str(instance.pk),
            objeto_repr=self.get_object_repr(instance),
            alteracoes=None,
            id_usuario=audit_info['id_usuario'],
            id_profissional=id_profissional,
            perfil=perfil,
            ip=audit_info['ip'],
            user_agent=audit_info['user_agent'],
            metodo_http=audit_info['metodo_http'],
            caminho=audit_info['caminho'],
        )

        return super().retrieve(request, *args, **kwargs)
