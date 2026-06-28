from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from neurocare_project.permissions import IsAdmin
from .models import AuditLog
from .serializers import AuditLogSerializer


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all().order_by('-data_hora')
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        'data_hora': ['gte', 'lte'],
        'id_usuario': ['exact'],
        'acao': ['exact'],
        'entidade': ['exact'],
        'objeto_id': ['exact'],
    }
    search_fields = ['usuario_login', 'objeto_repr']
    ordering_fields = ['data_hora', 'acao', 'entidade']
    ordering = ['-data_hora']
    pagination_class = None

    @action(detail=False, methods=['get'])
    def exportar(self, request):
        """
        Exportar logs em CSV ou XLSX.
        Query params: ?formato=csv|xlsx&<filtros>
        """
        formato = request.query_params.get('formato', 'csv').lower()

        queryset = self.filter_queryset(self.get_queryset())

        if formato == 'csv':
            return self._export_csv(queryset)
        elif formato == 'xlsx':
            return self._export_xlsx(queryset)
        else:
            return Response(
                {'detail': 'formato inválido (use csv ou xlsx)'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def _export_csv(self, queryset):
        import csv
        from io import StringIO
        from django.http import HttpResponse

        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow([
            'Data/Hora',
            'Usuário',
            'Perfil',
            'Ação',
            'Entidade',
            'Objeto',
            'ID Objeto',
            'Alterações',
            'IP',
        ])

        for log in queryset:
            alteracoes_str = str(log.alteracoes) if log.alteracoes else ''
            writer.writerow([
                log.data_hora.isoformat(),
                log.usuario_login,
                log.perfil or '',
                log.acao,
                log.entidade or '',
                log.objeto_repr or '',
                log.objeto_id or '',
                alteracoes_str,
                log.ip or '',
            ])

        response = HttpResponse(buffer.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="auditoria.csv"'
        return response

    def _export_xlsx(self, queryset):
        from openpyxl import Workbook
        from django.http import HttpResponse
        from io import BytesIO

        wb = Workbook()
        ws = wb.active
        ws.title = 'Auditoria'

        headers = [
            'Data/Hora',
            'Usuário',
            'Perfil',
            'Ação',
            'Entidade',
            'Objeto',
            'ID Objeto',
            'Alterações',
            'IP',
        ]
        ws.append(headers)

        for log in queryset:
            alteracoes_str = str(log.alteracoes) if log.alteracoes else ''
            ws.append([
                log.data_hora.isoformat(),
                log.usuario_login,
                log.perfil or '',
                log.acao,
                log.entidade or '',
                log.objeto_repr or '',
                log.objeto_id or '',
                alteracoes_str,
                log.ip or '',
            ])

        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        response = HttpResponse(
            buffer.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="auditoria.xlsx"'
        return response
