from neurocare_project.crud_views import make_crud_views

from .forms import TipoTransacaoForm
from .models import TipoTransacaoFinanceira

_views = make_crud_views(
    model=TipoTransacaoFinanceira,
    form_class=TipoTransacaoForm,
    list_template="tipos_transacao/list.html",
    row_template="tipos_transacao/row.html",
    form_template="tipos_transacao/form.html",
    form_partial_template="tipos_transacao/_form_partial.html",
    list_url_name="tipos_transacao:list",
    list_order_by=["nome"],
    create_title="Novo Tipo de Transação",
    edit_title_fn=lambda i: "Editar Tipo",
    enable_delete=True,
)

list_tipos = _views["list"]
create_tipo = _views["create"]
update_tipo = _views["update"]
delete_tipo = _views["delete"]
