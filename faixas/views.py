from neurocare_project.crud_views import make_crud_views
from pacientes.models import FaixaEtaria

from .forms import FaixaEtariaForm

_views = make_crud_views(
    model=FaixaEtaria,
    form_class=FaixaEtariaForm,
    list_template="faixas/list.html",
    row_template="faixas/row.html",
    form_template="faixas/form.html",
    form_partial_template="faixas/_form_partial.html",
    list_url_name="faixas:list",
    list_order_by=["nome"],
    create_title="Nova Faixa Etária",
    edit_title_fn=lambda i: f"Editar {i.nome}",
    item_context_name="faixa",
    list_context_name="faixas",
)

list_faixas = _views["list"]
create_faixa = _views["create"]
update_faixa = _views["update"]
