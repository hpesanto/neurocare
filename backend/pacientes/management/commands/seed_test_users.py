import hashlib

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from profissionais.models import PerfilAcesso, Profissional


class Command(BaseCommand):
    help = "Create test users with different profiles for permission testing"

    def handle(self, *args, **options):
        perfis = {p.nome: p for p in PerfilAcesso.objects.all()}

        test_users = [
            {
                "username": "psicologa1",
                "email": "psicologa1@neurocare.com",
                "password": "test123",
                "nome": "Dra. Ana Psicologa",
                "perfil": "Psicologo",
            },
            {
                "username": "psicologa2",
                "email": "psicologa2@neurocare.com",
                "password": "test123",
                "nome": "Dra. Beatriz Psicologa",
                "perfil": "Psicologo",
            },
            {
                "username": "secretaria",
                "email": "secretaria@neurocare.com",
                "password": "test123",
                "nome": "Julia Secretaria",
                "perfil": "Secretaria",
            },
        ]

        for u in test_users:
            django_user, created = User.objects.get_or_create(
                username=u["username"],
                defaults={
                    "email": u["email"],
                    "first_name": u["nome"].split()[0],
                    "last_name": " ".join(u["nome"].split()[1:]),
                },
            )
            if created:
                django_user.set_password(u["password"])
                django_user.save()

            perfil = perfis.get(u["perfil"])
            Profissional.objects.get_or_create(
                email=u["email"],
                defaults={
                    "nome": u["nome"],
                    "login": u["username"],
                    "senha_hash": hashlib.sha256(u["password"].encode()).hexdigest(),
                    "id_perfil_acesso": perfil,
                    "ativo": True,
                },
            )
            status = "created" if created else "exists"
            self.stdout.write(f"  {u['username']} ({u['perfil']}): {status}")
