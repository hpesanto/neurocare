import uuid

from django.db import models

from formas_cobranca_reabilitacao.models import FormaCobrancaReabilitacao
from pacientes.models import Paciente, Usuario


class ReabilitacaoNeuropsicologica(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, db_column="id_paciente"
    )
    id_psicologo = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, db_column="id_psicologo"
    )
    data_inicio = models.DateField()
    data_fim_prevista = models.DateField(blank=True, null=True)
    programa_descricao = models.TextField()
    num_sessoes_planejadas = models.IntegerField(blank=True, null=True)
    frequencia = models.CharField(max_length=100, blank=True, null=True)
    materiais_atividades_desc = models.TextField(blank=True, null=True)
    id_forma_cobranca = models.ForeignKey(
        FormaCobrancaReabilitacao,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_column="id_forma_cobranca",
    )
    valor_por_sessao = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    valor_total_pacote = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tb_reabilitacao_neuropsicologica"
        managed = False

    def __str__(self):
        return f"{self.id_paciente} - {self.data_inicio} ({self.id_psicologo})"
