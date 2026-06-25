import uuid

from django.db import models

from pacientes.models import Paciente, Usuario


class AvaliacaoNeuropsicologica(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, db_column="id_paciente"
    )
    id_psicologo = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, db_column="id_psicologo"
    )
    data_avaliacao = models.DateField()
    motivo_avaliacao = models.TextField()
    instrumentos_utilizados = models.TextField(blank=True, null=True)
    valor_avaliacao = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    hipoteses_diagnosticas = models.TextField(blank=True, null=True)
    resultados_principais = models.TextField(blank=True, null=True)
    conclusao_recomendacoes = models.TextField(blank=True, null=True)
    caminho_laudo_pdf = models.CharField(max_length=255, blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tb_avaliacao_neuropsicologica"
        managed = False

    def __str__(self):
        return f"{self.id_paciente} - {self.data_avaliacao} ({self.id_psicologo})"
