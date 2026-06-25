from neurocare_project.crud_views import make_crud_views
from pacientes.models import Produto

from .forms import ProdutoForm

_views = make_crud_views(
    model=Produto,
    form_class=ProdutoForm,
    list_template="produtos/list.html",
    row_template="produtos/row.html",
    form_template="produtos/form.html",
    form_partial_template="produtos/_form_partial.html",
    list_url_name="produtos:list",
    list_order_by=["nome"],
    create_title="Novo Produto",
    edit_title_fn=lambda i: f"Editar {i.nome}",
    item_context_name="produto",
    list_context_name="produtos",
)

list_produtos = _views["list"]
create_produto = _views["create"]
update_produto = _views["update"]
