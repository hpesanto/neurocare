from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.core.management import call_command
from io import StringIO
from auditoria.models import AuditLog


class AuditRetentionTestCase(TestCase):
    def test_purge_audit_logs_removes_old_logs(self):
        """Purge deve remover logs com mais de 365 dias."""
        now = timezone.now()

        # Criar log antigo (> 365 dias)
        old_log = AuditLog.objects.create(
            usuario_login='olduser',
            acao='CREATE',
            entidade='Paciente',
            objeto_id='1',
            objeto_repr='Old Patient',
        )
        old_log.data_hora = now - timedelta(days=400)
        old_log.save()

        # Criar log recente (< 365 dias)
        recent_log = AuditLog.objects.create(
            usuario_login='recentuser',
            acao='CREATE',
            entidade='Paciente',
            objeto_id='2',
            objeto_repr='Recent Patient',
        )
        recent_log.data_hora = now - timedelta(days=30)
        recent_log.save()

        self.assertEqual(AuditLog.objects.count(), 2)

        # Executar purge com 365 dias
        out = StringIO()
        call_command('purge_audit_logs', '--days', '365', stdout=out)

        # Verificar que apenas o log antigo foi removido
        self.assertEqual(AuditLog.objects.count(), 1)
        self.assertEqual(AuditLog.objects.first().usuario_login, 'recentuser')

        # Verificar mensagem de sucesso
        self.assertIn('Deleted 1 audit logs', out.getvalue())

    def test_purge_audit_logs_custom_days(self):
        """Purge com dias customizados deve funcionar."""
        now = timezone.now()

        # Criar logs em diferentes períodos
        log_90_days_ago = AuditLog.objects.create(
            usuario_login='user1',
            acao='CREATE',
            entidade='Paciente',
            objeto_id='1',
            objeto_repr='Patient 1',
        )
        log_90_days_ago.data_hora = now - timedelta(days=90)
        log_90_days_ago.save()

        log_30_days_ago = AuditLog.objects.create(
            usuario_login='user2',
            acao='CREATE',
            entidade='Paciente',
            objeto_id='2',
            objeto_repr='Patient 2',
        )
        log_30_days_ago.data_hora = now - timedelta(days=30)
        log_30_days_ago.save()

        self.assertEqual(AuditLog.objects.count(), 2)

        # Executar purge com 60 dias
        call_command('purge_audit_logs', '--days', '60')

        # Apenas o log de 90 dias atrás deve ser removido
        self.assertEqual(AuditLog.objects.count(), 1)
        self.assertEqual(AuditLog.objects.first().usuario_login, 'user2')

    def test_purge_audit_logs_does_not_remove_recent(self):
        """Purge não deve remover logs recentes."""
        now = timezone.now()

        # Criar logs recentes
        for i in range(5):
            log = AuditLog.objects.create(
                usuario_login=f'user{i}',
                acao='CREATE',
                entidade='Paciente',
                objeto_id=str(i),
                objeto_repr=f'Patient {i}',
            )
            log.data_hora = now - timedelta(days=10)
            log.save()

        self.assertEqual(AuditLog.objects.count(), 5)

        # Executar purge com 365 dias
        call_command('purge_audit_logs', '--days', '365')

        # Nenhum log deve ser removido
        self.assertEqual(AuditLog.objects.count(), 5)
