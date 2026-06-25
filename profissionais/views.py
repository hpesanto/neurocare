from neurocare_project.crud_views import make_crud_views

from .forms import ProfissionalForm
from .models import Profissional

_views = make_crud_views(
    model=Profissional,
    form_class=ProfissionalForm,
    list_template="profissionais/list.html",
    row_template="profissionais/row.html",
    form_template="profissionais/form.html",
    form_partial_template="profissionais/_form_partial.html",
    list_url_name="profissionais:list",
    list_order_by=["nome"],
    create_title="Novo Profissional",
    edit_title_fn=lambda i: f"Editar {i.nome}",
    item_context_name="profissional",
    list_context_name="profissionais",
)

list_profissionais = _views["list"]
create_profissional = _views["create"]
update_profissional = _views["update"]
