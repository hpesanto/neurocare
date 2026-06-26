from .permissions import get_perfil_nome, get_profissional


class OwnPatientsQuerysetMixin:
    patient_fk_field = "id_paciente"

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return qs
        perfil = get_perfil_nome(user)
        if perfil == "Administrador":
            return qs
        prof = get_profissional(user)
        if prof and perfil in ("Psicologo", "Psicóloga", "Psicólogo"):
            return qs.filter(**{f"{self.patient_fk_field}__id_psicologo_responsavel": prof.id})
        return qs


class OwnPsicologoQuerysetMixin:
    psicologo_fk_field = "id_psicologo"

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return qs
        perfil = get_perfil_nome(user)
        if perfil == "Administrador":
            return qs
        prof = get_profissional(user)
        if prof and perfil in ("Psicologo", "Psicóloga", "Psicólogo"):
            return qs.filter(**{self.psicologo_fk_field: prof.id})
        return qs
