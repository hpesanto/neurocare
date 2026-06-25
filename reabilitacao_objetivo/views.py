from neurocare_project.crud_views import make_crud_views

from .forms import ReabilitacaoObjetivoForm
from .models import ReabilitacaoObjetivo

_views = make_crud_views(
    model=ReabilitacaoObjetivo,
    form_class=ReabilitacaoObjetivoForm,
    list_template="reabilitacao_objetivo/list.html",
    row_template="reabilitacao_objetivo/row.html",
    form_template="reabilitacao_objetivo/form.html",
    form_partial_template="reabilitacao_objetivo/_form_partial.html",
    list_url_name="reabilitacao_objetivo:list",
    list_order_by=["-data_criacao"],
    create_title="Novo Objetivo",
    edit_title_fn=lambda i: "Editar Objetivo",
)

list_objetivos = _views["list"]
create_objetivo = _views["create"]
update_objetivo = _views["update"]
