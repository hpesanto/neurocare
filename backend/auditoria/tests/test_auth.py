from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from auditoria.models import AuditLog


class AuditAuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_successful_login_generates_audit_log(self):
        """Login bem-sucedido deve gerar evento LOGIN."""
        AuditLog.objects.all().delete()

        response = self.client.post(
            '/api/token/',
            {'username': 'testuser', 'password': 'testpass123'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        log = AuditLog.objects.filter(acao='LOGIN').first()
        self.assertIsNotNone(log)
        self.assertEqual(log.usuario_login, 'testuser')
        self.assertEqual(log.id_usuario, self.user.id)

    def test_failed_login_generates_audit_log(self):
        """Login com falha deve gerar evento LOGIN_FALHA."""
        AuditLog.objects.all().delete()

        response = self.client.post(
            '/api/token/',
            {'username': 'testuser', 'password': 'wrongpassword'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        log = AuditLog.objects.filter(acao='LOGIN_FALHA').first()
        self.assertIsNotNone(log)
        self.assertEqual(log.usuario_login, 'testuser')
        self.assertIsNone(log.id_usuario)

    def test_logout_generates_audit_log(self):
        """Logout deve gerar evento LOGOUT."""
        self.client.force_authenticate(user=self.user)

        refresh = RefreshToken.for_user(self.user)
        AuditLog.objects.all().delete()

        response = self.client.post(
            '/api/auth/logout/',
            {'refresh': str(refresh)},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

        log = AuditLog.objects.filter(acao='LOGOUT').first()
        self.assertIsNotNone(log)
        self.assertEqual(log.usuario_login, 'testuser')
        self.assertEqual(log.id_usuario, self.user.id)

    def test_logout_blacklists_refresh_token(self):
        """Logout deve invalidar o refresh token."""
        refresh = RefreshToken.for_user(self.user)
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            '/api/auth/logout/',
            {'refresh': str(refresh)},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

        # Tentar usar o refresh token deve falhar
        response = self.client.post(
            '/api/token/refresh/',
            {'refresh': str(refresh)},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
