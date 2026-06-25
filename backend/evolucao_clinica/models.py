import uuid

from django.db import models

from pacientes.models import Paciente, Usuario


class EvolucaoClinica(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, db_column="id_paciente"
    )
    id_psicologo = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, db_column="id_psicologo"
    )
    data_sessao = models.DateField()
    hora_sessao = models.TimeField(blank=True, null=True)
    evolucao_texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        # Keep unqualified table name so DB search_path (neurocare) resolves schema
        db_table = "tb_evolucao_clinica"
        managed = False

    def __str__(self):
        return f"{self.id_paciente} - {self.data_sessao} ({self.id_psicologo})"
