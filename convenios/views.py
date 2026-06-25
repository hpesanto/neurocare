from neurocare_project.crud_views import make_crud_views
from pacientes.models import Convenio

from .forms import ConvenioForm

_views = make_crud_views(
    model=Convenio,
    form_class=ConvenioForm,
    list_template="convenios/list.html",
    row_template="convenios/row.html",
    form_template="convenios/form.html",
    form_partial_template="convenios/_form_partial.html",
    list_url_name="convenios:list",
    list_order_by=["nome"],
    create_title="Novo Convênio",
    edit_title_fn=lambda i: f"Editar {i.nome}",
    item_context_name="convenio",
    list_context_name="convenios",
)

list_convenios = _views["list"]
create_convenio = _views["create"]
update_convenio = _views["update"]
