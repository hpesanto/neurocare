import csv
import io

from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes

from neurocare_project.permissions import IsPsicologaOrAdmin, get_perfil_nome, get_profissional

from .models import TransacaoFinanceira

COLUMNS = [
    ("Data", lambda t: str(t.data_transacao)),
    ("Paciente", lambda t: str(t.id_paciente) if t.id_paciente else ""),
    ("CPF Pagador", lambda t: t.cpf_pagador or ""),
    ("Endereco Pagador", lambda t: t.endereco_pagador or ""),
    ("Email Pagador", lambda t: t.email_pagador or ""),
    ("Tipo Transacao", lambda t: str(t.id_tipo_transacao) if t.id_tipo_transacao else ""),
    ("Descricao", lambda t: t.descricao or ""),
    ("Valor", lambda t: str(t.valor)),
    ("Forma Pagamento", lambda t: str(t.id_forma_pagamento) if t.id_forma_pagamento else ""),
    ("Status", lambda t: str(t.id_status_pagamento) if t.id_status_pagamento else ""),
    ("Observacoes", lambda t: t.observacoes or ""),
]


def _get_queryset(request):
    qs = TransacaoFinanceira.objects.select_related(
        "id_paciente", "id_tipo_transacao", "id_forma_pagamento", "id_status_pagamento",
    ).order_by("-data_transacao")

    user = request.user
    if not user.is_superuser and get_perfil_nome(user) != "Administrador":
        prof = get_profissional(user)
        if prof:
            qs = qs.filter(id_psicologo=prof.id)

    data_inicio = request.GET.get("data_inicio")
    data_fim = request.GET.get("data_fim")
    id_psicologo = request.GET.get("id_psicologo")
    id_tipo = request.GET.get("id_tipo_transacao")

    if data_inicio:
        qs = qs.filter(data_transacao__gte=data_inicio)
    if data_fim:
        qs = qs.filter(data_transacao__lte=data_fim)
    if id_psicologo:
        qs = qs.filter(id_psicologo=id_psicologo)
    if id_tipo:
        qs = qs.filter(id_tipo_transacao=id_tipo)

    return qs


@api_view(["GET"])
@permission_classes([IsPsicologaOrAdmin])
def exportar_transacoes(request):
    formato = request.GET.get("formato", "csv")
    qs = _get_queryset(request)
    headers = [c[0] for c in COLUMNS]
    rows = [[fn(t) for _, fn in COLUMNS] for t in qs]

    if formato == "xlsx":
        import openpyxl
        from openpyxl.styles import Font

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Transacoes"
        ws.append(headers)
        for cell in ws[1]:
            cell.font = Font(bold=True)
        for row in rows:
            ws.append(row)
        for col in ws.columns:
            max_len = max(len(str(c.value or "")) for c in col)
            ws.column_dimensions[col[0].column_letter].width = min(max_len + 2, 40)

        buf = io.BytesIO()
        wb.save(buf)
        buf.seek(0)
        resp = HttpResponse(buf.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        resp["Content-Disposition"] = "attachment; filename=transacoes.xlsx"
        return resp

    resp = HttpResponse(content_type="text/csv")
    resp["Content-Disposition"] = "attachment; filename=transacoes.csv"
    writer = csv.writer(resp)
    writer.writerow(headers)
    writer.writerows(rows)
    return resp
