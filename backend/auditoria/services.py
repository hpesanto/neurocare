import logging
from django.db import transaction
from .models import AuditLog


logger = logging.getLogger(__name__)


def registrar_log(
    usuario_login,
    acao,
    entidade=None,
    objeto_id=None,
    objeto_repr=None,
    alteracoes=None,
    id_usuario=None,
    id_profissional=None,
    perfil=None,
    ip=None,
    user_agent=None,
    metodo_http=None,
    caminho=None,
):
    """
    Registrar um evento de auditoria de forma best-effort.
    A falha na auditoria não quebra a operação (try/except).
    Executa após commit via transaction.on_commit().
    """
    def create_log():
        try:
            AuditLog.objects.create(
                usuario_login=usuario_login,
                acao=acao,
                entidade=entidade,
                objeto_id=objeto_id,
                objeto_repr=objeto_repr,
                alteracoes=alteracoes,
                id_usuario=id_usuario,
                id_profissional=id_profissional,
                perfil=perfil,
                ip=ip,
                user_agent=user_agent,
                metodo_http=metodo_http,
                caminho=caminho,
            )
        except Exception as e:
            logger.exception(f"Erro ao registrar auditoria ({acao}): {e}")

    transaction.on_commit(create_log)
