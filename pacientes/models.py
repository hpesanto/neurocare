import uuid

from django.db import models

try:
    from django.contrib.postgres.fields import ArrayField
except Exception:
    ArrayField = None


class Paciente(models.Model):
    # Store primary key as UUID; Django side default uses uuid.uuid4.
    # Note: Meta.managed=False means Django will not create this table automatically.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Explicit default manager to satisfy static analysis and make usage explicit
    objects = models.Manager()
    cpf = models.CharField(max_length=20, blank=True, null=True)
    nome = models.CharField(max_length=255)
    rg = models.CharField(max_length=50, blank=True, null=True)
    # genero stored as an array in the DB (existing schema). Use ArrayField when available.
    if ArrayField is not None:
        genero = ArrayField(models.CharField(max_length=50), blank=True, null=True)
    else:
        # Fallback to CharField for environments without postgres ArrayField support
        genero = models.CharField(max_length=50, blank=True, null=True)
    estado_civil = models.CharField(max_length=50, blank=True, null=True)
    profissao = models.CharField(max_length=100, blank=True, null=True)
    tel_1 = models.CharField(max_length=50, blank=True, null=True)
    tel_2 = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    logradouro = models.CharField(max_length=255, blank=True, null=True)
    num_fachada = models.CharField(max_length=50, blank=True, null=True)
    complemento = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=255, blank=True, null=True)
    municipio = models.CharField(max_length=255, blank=True, null=True)
    uf = models.CharField(max_length=2, blank=True, null=True)
    cep = models.CharField(max_length=20, blank=True, null=True)
    contato_emergencia = models.CharField(max_length=255, blank=True, null=True)
    tel_contato_emergencia = models.CharField(max_length=50, blank=True, null=True)
    parentesco_contato_emergencia = models.CharField(
        max_length=100, blank=True, null=True
    )

    class Meta:
        db_table = "paciente"
        managed = False

    def __str__(self):
        return f"{self.nome} ({self.cpf})"

    @property
    def genero_display(self):
        """Return a human-friendly string for genero whether it's stored as list or string."""
        val = self.genero
        if val is None:
            return ""
        if isinstance(val, (list, tuple)):
            return ", ".join([str(x) for x in val if x is not None and x != ""])
        return str(val)
