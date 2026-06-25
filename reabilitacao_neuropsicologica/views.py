from neurocare_project.crud_views import make_crud_views

from .forms import ReabilitacaoNeuropsicologicaForm
from .models import ReabilitacaoNeuropsicologica

_views = make_crud_views(
    model=ReabilitacaoNeuropsicologica,
    form_class=ReabilitacaoNeuropsicologicaForm,
    list_template="reabilitacao_neuropsicologica/list.html",
    row_template="reabilitacao_neuropsicologica/row.html",
    form_template="reabilitacao_neuropsicologica/form.html",
    form_partial_template="reabilitacao_neuropsicologica/_form_partial.html",
    list_url_name="reabilitacao:list",
    list_order_by=["-data_inicio"],
    create_title="Nova Reabilitação",
    edit_title_fn=lambda i: "Editar Reabilitação",
)

list_reabilitacao = _views["list"]
create_reabilitacao = _views["create"]
update_reabilitacao = _views["update"]
