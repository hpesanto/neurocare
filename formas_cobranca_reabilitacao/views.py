from neurocare_project.crud_views import make_crud_views

from .forms import FormaCobrancaReabilitacaoForm
from .models import FormaCobrancaReabilitacao

_views = make_crud_views(
    model=FormaCobrancaReabilitacao,
    form_class=FormaCobrancaReabilitacaoForm,
    list_template="formas_cobranca_reabilitacao/list.html",
    row_template="formas_cobranca_reabilitacao/row.html",
    form_template="formas_cobranca_reabilitacao/form.html",
    form_partial_template="formas_cobranca_reabilitacao/_form_partial.html",
    list_url_name="formas_cobranca:list",
    list_order_by=["nome"],
    create_title="Nova Forma de Cobrança",
    edit_title_fn=lambda i: "Editar Forma",
)

list_formas = _views["list"]
create_forma = _views["create"]
update_forma = _views["update"]
