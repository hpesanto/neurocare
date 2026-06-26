from rest_framework.permissions import BasePermission

from profissionais.models import Profissional


def get_profissional(user):
    if not user or not user.is_authenticated:
        return None
    try:
        return Profissional.objects.select_related("id_perfil_acesso").get(email=user.email)
    except Profissional.DoesNotExist:
        return None


def get_perfil_nome(user):
    if user.is_superuser:
        return "Administrador"
    prof = get_profissional(user)
    if prof and prof.id_perfil_acesso:
        return prof.id_perfil_acesso.nome
    return None


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or get_perfil_nome(request.user) == "Administrador"


class IsPsicologaOrAdmin(BasePermission):
    def has_permission(self, request, view):
        perfil = get_perfil_nome(request.user)
        return perfil in ("Administrador", "Psicologo", "Psicóloga", "Psicólogo")


class IsSecretariaOrAbove(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated


class DenyAll(BasePermission):
    def has_permission(self, request, view):
        return False


class ReadOnlyForSecretaria(BasePermission):
    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        perfil = get_perfil_nome(request.user)
        return perfil in ("Administrador", "Psicologo", "Psicóloga", "Psicólogo")
