from django.contrib import admin
from django.utils.html import format_html
import json
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        'data_hora',
        'acao_colored',
        'usuario_login',
        'entidade',
        'objeto_repr',
        'ip',
    )
    list_filter = ('acao', 'data_hora', 'entidade')
    search_fields = ('usuario_login', 'objeto_repr', 'ip')
    readonly_fields = (
        'id',
        'data_hora',
        'usuario_login',
        'acao',
        'entidade',
        'objeto_id',
        'objeto_repr',
        'alteracoes_pretty',
        'ip',
        'user_agent',
        'metodo_http',
        'caminho',
    )
    fieldsets = (
        ('Informações de Auditoria', {
            'fields': (
                'id',
                'data_hora',
                'acao',
                'usuario_login',
                'id_usuario',
                'id_profissional',
                'perfil',
            )
        }),
        ('Objeto Auditado', {
            'fields': (
                'entidade',
                'objeto_id',
                'objeto_repr',
            )
        }),
        ('Alterações', {
            'fields': ('alteracoes_pretty',),
        }),
        ('Requisição', {
            'fields': (
                'ip',
                'user_agent',
                'metodo_http',
                'caminho',
            )
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def acao_colored(self, obj):
        colors = {
            'LOGIN': '#28a745',
            'LOGIN_FALHA': '#dc3545',
            'LOGOUT': '#ffc107',
            'CREATE': '#17a2b8',
            'UPDATE': '#007bff',
            'DELETE': '#e83e8c',
            'LEITURA': '#6c757d',
        }
        color = colors.get(obj.acao, '#999')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_acao_display()
        )
    acao_colored.short_description = 'Ação'

    def alteracoes_pretty(self, obj):
        if not obj.alteracoes:
            return '-'
        return format_html(
            '<pre style="background: #f5f5f5; padding: 10px; border-radius: 5px;">{}</pre>',
            json.dumps(obj.alteracoes, indent=2, ensure_ascii=False)
        )
    alteracoes_pretty.short_description = 'Alterações'
