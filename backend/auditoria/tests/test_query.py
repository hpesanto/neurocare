from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from auditoria.models import AuditLog
from profissionais.models import Profissional


class AuditQueryTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Criar usuário Admin
        self.admin_user = User.objects.create_user(
            username='admin', password='adminpass'
        )
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_user.save()

        # Criar profissional Admin
        self.admin_prof = Profissional.objects.create(
            usuario=self.admin_user,
            nome_completo='Admin User',
            cpf='11111111111',
            tipo_profissional='Administrador',
        )

        # Criar usuário não-admin
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.user.is_staff = False
        self.user.save()

        # Criar alguns logs
        AuditLog.objects.create(
            usuario_login='testuser',
            acao='CREATE',
            entidade='Paciente',
            objeto_id='1',
            objeto_repr='João Silva',
            usuario_login='testuser',
            ip='192.168.1.1',
        )

        AuditLog.objects.create(
            usuario_login='testuser',
            acao='UPDATE',
            entidade='Paciente',
            objeto_id='1',
            objeto_repr='João Silva',
            ip='192.168.1.1',
            alteracoes={'email': {'de': 'old@example.com', 'para': 'new@example.com'}},
        )

    def test_non_admin_cannot_access_audit_logs(self):
        """Usuário não-admin deve receber 403."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/auditoria/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_access_audit_logs(self):
        """Admin deve ter acesso aos logs."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/auditoria/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_filter_by_action(self):
        """Filtrar por ação deve funcionar."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/auditoria/?acao=CREATE')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['acao'], 'CREATE')

    def test_filter_by_entity(self):
        """Filtrar por entidade deve funcionar."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/auditoria/?entidade=Paciente')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_search_by_username(self):
        """Buscar por nome de usuário deve funcionar."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/auditoria/?search=testuser')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_export_csv(self):
        """Exportar em CSV deve funcionar."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/auditoria/exportar/?formato=csv')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('auditoria.csv', response['Content-Disposition'])

    def test_export_xlsx(self):
        """Exportar em XLSX deve funcionar."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/auditoria/exportar/?formato=xlsx')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('spreadsheet', response['Content-Type'])
        self.assertIn('auditoria.xlsx', response['Content-Disposition'])

    def test_audit_log_is_immutable(self):
        """Logs não devem ser editáveis ou deletáveis."""
        self.client.force_authenticate(user=self.admin_user)
        log = AuditLog.objects.first()

        # Tentar editar
        response = self.client.patch(f'/api/auditoria/{log.id}/', {'acao': 'DELETE'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # Tentar deletar
        response = self.client.delete(f'/api/auditoria/{log.id}/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
