from neurocare_project.crud_views import make_crud_views
from pacientes.models import ContatoEmergencia

from .forms import ContatoEmergenciaForm

_views = make_crud_views(
    model=ContatoEmergencia,
    form_class=ContatoEmergenciaForm,
    list_template="contatos_emergencia/list.html",
    row_template="contatos_emergencia/row.html",
    form_template="contatos_emergencia/form.html",
    form_partial_template="contatos_emergencia/_form_partial.html",
    list_url_name="contatos_emergencia:list",
    list_order_by=["nome_contato"],
    create_title="Novo Contato de Emergência",
    edit_title_fn=lambda i: f"Editar {i.nome_contato}",
    item_context_name="contato",
    list_context_name="contatos",
)

list_contatos = _views["list"]
create_contato = _views["create"]
update_contato = _views["update"]
