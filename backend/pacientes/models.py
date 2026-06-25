import uuid

from django.db import models

try:
    from django.contrib.postgres.fields import ArrayField
except Exception:
    ArrayField = None


class Usuario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome_completo = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    login = models.CharField(max_length=100, unique=True)
    senha_hash = models.CharField(max_length=255)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Return the full name so ModelChoiceField/Select shows a readable label
        return self.nome_completo or str(self.id)

    class Meta:
        db_table = "tb_usuario"
        managed = False


class Convenio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100, unique=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tb_convenio"
        managed = False

    def __str__(self):
        return self.nome or str(self.id)


class FormaPagamento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100, unique=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tb_forma_pagamento"
        managed = False

    def __str__(self):
        return self.nome or str(self.id)


class TipoProduto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100, unique=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tb_tipo_produto"
        managed = False

    def __str__(self):
        return self.nome or str(self.id)


class TipoServico(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100, unique=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tb_tipo_servico"
        managed = False

    def __str__(self):
        return self.nome or str(self.id)


class FaixaEtaria(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tb_faixa_etaria"
        managed = False

    def __str__(self):
        return self.nome or str(self.id)


class Paciente(models.Model):
    GENERO_CHOICES = [
        ("Masculino", "Masculino"),
        ("Feminino", "Feminino"),
        ("Outro", "Outro"),
        ("Não Informar", "Não Informar"),
    ]

    ESTADO_CIVIL_CHOICES = [
        ("Solteiro", "Solteiro"),
        ("Casado", "Casado"),
        ("Divorciado", "Divorciado"),
        ("Viúvo", "Viúvo"),
        ("União Estável", "União Estável"),
    ]

    STATUS_CHOICES = [
        ("Ativo", "Ativo"),
        ("Inativo", "Inativo"),
        ("Alta", "Alta"),
        ("Em Espera", "Em Espera"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome_completo = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    genero = models.CharField(max_length=50, choices=GENERO_CHOICES)
    estado_civil = models.CharField(max_length=50, choices=ESTADO_CIVIL_CHOICES)
    profissao = models.CharField(max_length=100, blank=True, null=True)
    telefone_principal = models.CharField(max_length=20)
    telefone_secundario = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    endereco_rua = models.CharField(max_length=255, blank=True, null=True)
    endereco_numero = models.CharField(max_length=50, blank=True, null=True)
    endereco_complemento = models.CharField(max_length=100, blank=True, null=True)
    endereco_bairro = models.CharField(max_length=100, blank=True, null=True)
    endereco_cidade = models.CharField(max_length=100, blank=True, null=True)
    endereco_estado = models.CharField(max_length=50, blank=True, null=True)
    endereco_cep = models.CharField(max_length=10, blank=True, null=True)
    id_psicologo_responsavel = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="pacientes_responsaveis",
        db_column="id_psicologo_responsavel",
    )
    quem_encaminhou = models.CharField(max_length=255, blank=True, null=True)
    motivo_encaminhamento = models.TextField(blank=True, null=True)
    id_convenio = models.ForeignKey(
        Convenio,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_column="id_convenio",
    )
    numero_carteirinha_convenio = models.CharField(
        max_length=100, blank=True, null=True
    )
    validade_carteirinha_convenio = models.DateField(blank=True, null=True)
    id_faixa_etaria = models.ForeignKey(
        FaixaEtaria,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_column="id_faixa_etaria",
    )
    status_paciente = models.CharField(max_length=50, choices=STATUS_CHOICES)
    observacoes_gerais = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tb_paciente"
        managed = False

    def __str__(self):
        return f"{self.nome_completo} ({self.cpf or 'Sem CPF'})"


class Produto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_tipo_produto = models.ForeignKey(
        TipoProduto,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_column="id_tipo_produto",
    )
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tb_produto"
        managed = False

    def __str__(self):
        return self.nome or str(self.id)


class ContatoEmergencia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_paciente = models.ForeignKey(
        "Paciente",
        on_delete=models.CASCADE,
        db_column="id_paciente",
    )
    nome_contato = models.CharField(max_length=255)
    telefone_contato = models.CharField(max_length=20)
    parentesco = models.CharField(max_length=100)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tb_contato_emergencia"
        managed = False

    def __str__(self):
        return f"{self.nome_contato} ({self.telefone_contato})"


class PacienteServico(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_paciente = models.ForeignKey(
        "Paciente",
        on_delete=models.CASCADE,
        db_column="id_paciente",
    )
    id_tipo_servico = models.ForeignKey(
        "TipoServico",
        on_delete=models.CASCADE,
        db_column="id_tipo_servico",
    )
    psicologo_responsavel_servico = models.ForeignKey(
        "Usuario",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_column="id_psicologo_responsavel_servico",
    )
    data_inicio = models.DateField(default=__import__("datetime").date.today)
    data_fim = models.DateField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    observacoes = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tb_paciente_servico"
        managed = False
        constraints = [
            models.UniqueConstraint(
                fields=["id_paciente", "id_tipo_servico"],
                name="unique_paciente_tipo_servico",
            ),
        ]

    def __str__(self):
        return f"{self.id_paciente} - {self.id_tipo_servico}"
