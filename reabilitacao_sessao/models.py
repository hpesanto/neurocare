import uuid

from django.db import models

from reabilitacao_neuropsicologica.models import ReabilitacaoNeuropsicologica


class ReabilitacaoSessao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_reabilitacao = models.ForeignKey(
        ReabilitacaoNeuropsicologica,
        on_delete=models.CASCADE,
        db_column="id_reabilitacao",
    )
    data_sessao = models.DateField()
    hora_sessao = models.TimeField(blank=True, null=True)
    passos_realizados = models.TextField()
    proximos_passos_planejamento = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tb_reabilitacao_sessao"
        managed = False

    def __str__(self):
        return f"{self.id_reabilitacao} - {self.data_sessao}"
