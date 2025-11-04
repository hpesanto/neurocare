import uuid

from django.db import models

from reabilitacao_neuropsicologica.models import ReabilitacaoNeuropsicologica
from status_objetivo_reabilitacao.models import StatusObjetivoReabilitacao


class ReabilitacaoObjetivo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_reabilitacao = models.ForeignKey(
        ReabilitacaoNeuropsicologica,
        on_delete=models.CASCADE,
        db_column="id_reabilitacao",
    )
    descricao = models.TextField()
    id_status_objetivo = models.ForeignKey(
        StatusObjetivoReabilitacao,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_column="id_status_objetivo",
    )
    comentario_status = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tb_reabilitacao_objetivo"
        managed = False

    def __str__(self):
        return f"Objetivo {self.id} - {str(self.descricao)[:40]}"
