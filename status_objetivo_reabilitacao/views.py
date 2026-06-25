from neurocare_project.crud_views import make_crud_views

from .forms import StatusObjetivoReabilitacaoForm
from .models import StatusObjetivoReabilitacao

_views = make_crud_views(
    model=StatusObjetivoReabilitacao,
    form_class=StatusObjetivoReabilitacaoForm,
    list_template="status_objetivo_reabilitacao/list.html",
    row_template="status_objetivo_reabilitacao/row.html",
    form_template="status_objetivo_reabilitacao/form.html",
    form_partial_template="status_objetivo_reabilitacao/_form_partial.html",
    list_url_name="status:list",
    list_order_by=["nome"],
    create_title="Novo Status",
    edit_title_fn=lambda i: "Editar Status",
)

list_status = _views["list"]
create_status = _views["create"]
update_status = _views["update"]
