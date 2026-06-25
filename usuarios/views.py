from neurocare_project.crud_views import make_crud_views
from profissionais.models import Profissional

from .forms import UsuarioForm

_views = make_crud_views(
    model=Profissional,
    form_class=UsuarioForm,
    list_template="usuarios/list.html",
    row_template="usuarios/row.html",
    form_template="usuarios/form.html",
    form_partial_template="usuarios/_form_partial.html",
    list_url_name="usuarios:list",
    list_order_by=["nome"],
    create_title="Novo Usuário",
    edit_title_fn=lambda i: f"Editar {i.nome}",
    item_context_name="usuario",
    list_context_name="usuarios",
)

list_usuarios = _views["list"]
create_usuario = _views["create"]
update_usuario = _views["update"]
