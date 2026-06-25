from neurocare_project.crud_views import make_crud_views
from pacientes.models import TipoProduto

from .forms import TipoProdutoForm

_views = make_crud_views(
    model=TipoProduto,
    form_class=TipoProdutoForm,
    list_template="tipos_produto/list.html",
    row_template="tipos_produto/row.html",
    form_template="tipos_produto/form.html",
    form_partial_template="tipos_produto/_form_partial.html",
    list_url_name="tipos_produto:list",
    list_order_by=["nome"],
    create_title="Novo Tipo de Produto",
    edit_title_fn=lambda i: f"Editar {i.nome}",
    item_context_name="tipo",
    list_context_name="tipos",
)

list_tipos = _views["list"]
create_tipo = _views["create"]
update_tipo = _views["update"]
