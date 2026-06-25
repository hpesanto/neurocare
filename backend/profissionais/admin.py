from django.contrib import admin

from .models import Profissional


@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    # Only include fields that are actual DB columns on tb_usuario
    list_display = ("nome", "email", "id_perfil_acesso")
    search_fields = ("nome", "email")
    list_filter = ("id_perfil_acesso",)
