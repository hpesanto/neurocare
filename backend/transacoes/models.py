import uuid

from django.db import models

from pacientes.models import FormaPagamento, Paciente, Usuario
from status_pagamento.models import StatusPagamento
from tipos_transacao.models import TipoTransacaoFinanceira

try:
    from evolucao_clinica.models import EvolucaoClinica
except Exception:
    EvolucaoClinica = None

try:
    from avaliacao_neuropsicologica.models import AvaliacaoNeuropsicologica
except Exception:
    AvaliacaoNeuropsicologica = None

try:
    from reabilitacao_neuropsicologica.models import ReabilitacaoNeuropsicologica
except Exception:
    ReabilitacaoNeuropsicologica = None

try:
    from reabilitacao_sessao.models import ReabilitacaoSessao
except Exception:
    ReabilitacaoSessao = None

try:
    from vendas.models import VendaVinculada
except Exception:
    VendaVinculada = None

try:
    from vendas_geral.models import VendaGeral
except Exception:
    VendaGeral = None


class TransacaoFinanceira(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_paciente = models.ForeignKey(
        Paciente,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_column="id_paciente",
    )
    id_psicologo = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_column="id_psicologo",
    )
    id_tipo_transacao = models.ForeignKey(
        TipoTransacaoFinanceira, on_delete=models.CASCADE, db_column="id_tipo_transacao"
    )
    data_transacao = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    id_forma_pagamento = models.ForeignKey(
        FormaPagamento, on_delete=models.CASCADE, db_column="id_forma_pagamento"
    )
    id_status_pagamento = models.ForeignKey(
        StatusPagamento, on_delete=models.CASCADE, db_column="id_status_pagamento"
    )
    descricao = models.TextField()
    cpf_pagador = models.CharField(max_length=14, blank=True, null=True)
    endereco_pagador = models.TextField(blank=True, null=True)
    email_pagador = models.CharField(max_length=255, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)

    id_evolucao_clinica = (
        models.ForeignKey(
            EvolucaoClinica,
            on_delete=models.SET_NULL,
            blank=True,
            null=True,
            db_column="id_evolucao_clinica",
        )
        if EvolucaoClinica
        else models.UUIDField(blank=True, null=True)
    )

    id_avaliacao_neuropsicologica = (
        models.ForeignKey(
            AvaliacaoNeuropsicologica,
            on_delete=models.SET_NULL,
            blank=True,
            null=True,
            db_column="id_avaliacao_neuropsicologica",
        )
        if AvaliacaoNeuropsicologica
        else models.UUIDField(blank=True, null=True)
    )

    id_reabilitacao_neuropsicologica = (
        models.ForeignKey(
            ReabilitacaoNeuropsicologica,
            on_delete=models.SET_NULL,
            blank=True,
            null=True,
            db_column="id_reabilitacao_neuropsicologica",
        )
        if ReabilitacaoNeuropsicologica
        else models.UUIDField(blank=True, null=True)
    )

    id_reabilitacao_sessao = (
        models.ForeignKey(
            ReabilitacaoSessao,
            on_delete=models.SET_NULL,
            blank=True,
            null=True,
            db_column="id_reabilitacao_sessao",
        )
        if ReabilitacaoSessao
        else models.UUIDField(blank=True, null=True)
    )

    id_venda_vinculada_paciente = (
        models.ForeignKey(
            VendaVinculada,
            on_delete=models.SET_NULL,
            blank=True,
            null=True,
            db_column="id_venda_vinculada_paciente",
        )
        if VendaVinculada
        else models.UUIDField(blank=True, null=True)
    )

    id_venda_geral = (
        models.ForeignKey(
            VendaGeral,
            on_delete=models.SET_NULL,
            blank=True,
            null=True,
            db_column="id_venda_geral",
        )
        if VendaGeral
        else models.UUIDField(blank=True, null=True)
    )

    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tb_transacao_financeira"
        managed = False

    def __str__(self):
        return f"Transacao {self.id} - {self.data_transacao} - {self.valor}"
