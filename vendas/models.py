import uuid

from django.db import models

from pacientes.models import FormaPagamento, Paciente, Produto, Usuario


class VendaVinculada(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, db_column="id_paciente"
    )
    id_psicologo = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_column="id_psicologo",
    )
    id_produto = models.ForeignKey(
        Produto, on_delete=models.CASCADE, db_column="id_produto"
    )
    data_venda = models.DateField()
    quantidade = models.IntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total_produto = models.DecimalField(max_digits=10, decimal_places=2)
    id_forma_pagamento = models.ForeignKey(
        FormaPagamento, on_delete=models.CASCADE, db_column="id_forma_pagamento"
    )
    observacoes = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tb_venda_vinculada_paciente"
        managed = False

    def __str__(self):
        return f"{self.id_paciente} - {self.data_venda} - {self.id_produto}"
