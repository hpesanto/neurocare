import uuid

from django.db import models

from pacientes.models import FormaPagamento, Usuario


class VendaGeral(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_psicologo = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_column="id_psicologo",
    )
    data_venda = models.DateField()
    nome_comprador = models.CharField(max_length=255, blank=True, null=True)
    contato_comprador = models.CharField(max_length=255, blank=True, null=True)
    valor_total_transacao = models.DecimalField(max_digits=10, decimal_places=2)
    id_forma_pagamento = models.ForeignKey(
        FormaPagamento, on_delete=models.CASCADE, db_column="id_forma_pagamento"
    )
    observacoes = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tb_venda_geral"
        managed = False

    def __str__(self):
        return f"VendaGeral {self.id} - {self.data_venda}"


class VendaGeralItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_venda_geral = models.ForeignKey(
        VendaGeral, on_delete=models.CASCADE, db_column="id_venda_geral"
    )
    id_produto = models.ForeignKey(
        "pacientes.Produto", on_delete=models.CASCADE, db_column="id_produto"
    )
    quantidade = models.IntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total_item = models.DecimalField(max_digits=10, decimal_places=2)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tb_venda_geral_item"
        managed = False

    def __str__(self):
        return f"Item {self.id} - {self.id_produto} x {self.quantidade}"
