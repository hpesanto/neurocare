from django.db import models
from django.contrib.auth.models import User


class AuditLog(models.Model):
    ACAO_CHOICES = (
        ('LOGIN', 'Login'),
        ('LOGIN_FALHA', 'Login Falha'),
        ('LOGOUT', 'Logout'),
        ('CREATE', 'Criação'),
        ('UPDATE', 'Alteração'),
        ('DELETE', 'Exclusão'),
        ('LEITURA', 'Leitura'),
    )

    id = models.BigAutoField(primary_key=True)
    data_hora = models.DateTimeField(auto_now_add=True, db_index=True)
    id_usuario = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, db_index=True
    )
    usuario_login = models.CharField(max_length=150)
    id_profissional = models.IntegerField(null=True, blank=True)
    perfil = models.CharField(max_length=50, null=True, blank=True)
    acao = models.CharField(max_length=20, choices=ACAO_CHOICES)
    entidade = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    objeto_id = models.CharField(max_length=64, null=True, blank=True)
    objeto_repr = models.CharField(max_length=255, null=True, blank=True)
    alteracoes = models.JSONField(null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)
    metodo_http = models.CharField(max_length=10, null=True, blank=True)
    caminho = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'tb_log_auditoria'
        indexes = [
            models.Index(fields=['data_hora']),
            models.Index(fields=['id_usuario']),
            models.Index(fields=['entidade', 'objeto_id']),
            models.Index(fields=['acao']),
        ]

    def __str__(self):
        return f"{self.acao} - {self.usuario_login} - {self.data_hora}"
