import uuid

from django.db import models


class PerfilAcesso(models.Model):
    """Minimal model mapping to existing `tb_perfil_acesso` table.

    The canonical DDL is available in `documentacao/ddls.sql`. This model is
    read-only from Django's perspective (managed=False).
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=50)
    descricao = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tb_perfil_acesso"
        managed = False

    def __str__(self):
        return str(self.nome)


class Profissional(models.Model):
    """Model mapping to `neurocare.tb_usuario` (tb_usuario) DDL supplied by the user.

    The model is intentionally marked managed=False because the database already
    contains the table definition.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_perfil_acesso = models.ForeignKey(
        PerfilAcesso, on_delete=models.PROTECT, db_column="id_perfil_acesso"
    )

    # keep a 'nome' attribute for backward compatibility in templates and queries
    nome = models.CharField(max_length=255, db_column="nome_completo")
    email = models.EmailField(max_length=255, unique=True)
    login = models.CharField(max_length=100, unique=True)
    senha_hash = models.CharField(max_length=255, db_column="senha_hash")
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        db_table = "tb_usuario"
        managed = False

    def __str__(self):
        return str(self.nome)

    # Backwards-compatible properties (some templates may still reference them)
    @property
    def cpf(self):
        return None

    @property
    def especialidade(self):
        return None

    @property
    def celular(self):
        return None

    @property
    def whatsapp(self):
        return False

    @property
    def telefone(self):
        return None

    # Backwards compatibility: expose nome_completo as property
    @property
    def nome_completo(self):
        return self.nome
