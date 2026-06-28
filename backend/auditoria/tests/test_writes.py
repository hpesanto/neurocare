from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from pacientes.models import Paciente
from auditoria.models import AuditLog


class AuditWritesTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_create_generates_audit_log(self):
        """Criar um paciente deve gerar evento CREATE."""
        data = {
            'nome_completo': 'João Silva',
            'cpf': '12345678901',
            'data_nascimento': '1990-01-01',
            'email': 'joao@example.com',
            'genero': 'M',
        }
        response = self.client.post('/api/pacientes/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        log = AuditLog.objects.filter(acao='CREATE', entidade='Paciente').first()
        self.assertIsNotNone(log)
        self.assertEqual(log.usuario_login, 'testuser')
        self.assertEqual(log.objeto_repr, 'João Silva')
        self.assertIsNotNone(log.alteracoes)

    def test_update_generates_audit_log_with_diff(self):
        """Editar um paciente deve gerar evento UPDATE com diff."""
        paciente = Paciente.objects.create(
            nome_completo='Maria Silva',
            cpf='12345678902',
            data_nascimento='1992-01-01',
            email='maria@example.com',
            genero='F',
        )

        AuditLog.objects.all().delete()

        data = {'email': 'maria.silva@example.com'}
        response = self.client.patch(f'/api/pacientes/{paciente.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        log = AuditLog.objects.filter(acao='UPDATE', entidade='Paciente').first()
        self.assertIsNotNone(log)
        self.assertIn('email', log.alteracoes)
        self.assertEqual(log.alteracoes['email']['de'], 'maria@example.com')
        self.assertEqual(log.alteracoes['email']['para'], 'maria.silva@example.com')

    def test_delete_generates_audit_log(self):
        """Deletar um paciente deve gerar evento DELETE."""
        paciente = Paciente.objects.create(
            nome_completo='Carlos Silva',
            cpf='12345678903',
            data_nascimento='1991-01-01',
            email='carlos@example.com',
            genero='M',
        )

        AuditLog.objects.all().delete()

        response = self.client.delete(f'/api/pacientes/{paciente.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        log = AuditLog.objects.filter(acao='DELETE', entidade='Paciente').first()
        self.assertIsNotNone(log)
        self.assertEqual(log.usuario_login, 'testuser')
        self.assertIsNone(log.alteracoes)

    def test_sensitive_fields_not_logged(self):
        """Campos sensíveis não devem ser registrados no log."""
        data = {
            'nome_completo': 'Test User',
            'cpf': '12345678904',
            'data_nascimento': '1993-01-01',
            'email': 'test@example.com',
            'genero': 'M',
        }
        response = self.client.post('/api/pacientes/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        log = AuditLog.objects.filter(acao='CREATE', entidade='Paciente').first()
        self.assertIsNotNone(log)

        # Verificar que campos sensíveis não estão no log
        alteracoes_str = str(log.alteracoes)
        self.assertNotIn('password', alteracoes_str.lower())
        self.assertNotIn('token', alteracoes_str.lower())
