import uuid

from django.db import models

from pacientes.models import Paciente, Usuario


class Agendamento(models.Model):
    TIPO_CHOICES = [
        ("Avaliacao", "Avaliação"),
        ("Reabilitacao", "Reabilitação"),
        ("Psicoterapia", "Psicoterapia"),
        ("Outro", "Outro"),
    ]
    SALA_CHOICES = [(1, "Sala 1"), (2, "Sala 2"), (3, "Sala 3")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_profissional = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, db_column="id_profissional",
    )
    id_paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, db_column="id_paciente",
    )
    sala = models.IntegerField(choices=SALA_CHOICES)
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, default="Psicoterapia")
    observacoes = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tb_agendamento"
        managed = False

    def __str__(self):
        return f"{self.data} {self.hora_inicio}-{self.hora_fim} Sala {self.sala}"
