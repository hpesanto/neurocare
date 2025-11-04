import uuid

from django.db import models


class StatusObjetivoReabilitacao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100, unique=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tb_status_objetivo_reabilitacao"
        managed = False

    def __str__(self):
        return self.nome
