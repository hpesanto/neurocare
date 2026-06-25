from neurocare_project.crud_views import make_crud_views

from .forms import TransacaoFinanceiraForm
from .models import TransacaoFinanceira

_views = make_crud_views(
    model=TransacaoFinanceira,
    form_class=TransacaoFinanceiraForm,
    list_template="transacoes/list.html",
    row_template="transacoes/row.html",
    form_template="transacoes/form.html",
    form_partial_template="transacoes/_form_partial.html",
    list_url_name="transacoes:list",
    list_order_by=["-data_transacao"],
    create_title="Nova Transação",
    edit_title_fn=lambda i: "Editar Transação",
)

list_transacoes = _views["list"]
create_transacao = _views["create"]
update_transacao = _views["update"]
