import uuid

from django.db import models


class StatusPagamento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=50, unique=True)
    data_criacao = models.DateTimeField(null=True, blank=True)
    data_atualizacao = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "tb_status_pagamento"
        managed = False

    def __str__(self):
        return self.nome
        return self.nome
