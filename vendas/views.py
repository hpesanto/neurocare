from neurocare_project.crud_views import make_crud_views

from .forms import VendaVinculadaForm
from .models import VendaVinculada

_views = make_crud_views(
    model=VendaVinculada,
    form_class=VendaVinculadaForm,
    list_template="vendas_vinculadas/list.html",
    row_template="vendas_vinculadas/row.html",
    form_template="vendas_vinculadas/form.html",
    form_partial_template="vendas_vinculadas/_form_partial.html",
    list_url_name="vendas:list",
    list_order_by=["-data_venda"],
    create_title="Nova Venda Vinculada",
    edit_title_fn=lambda i: "Editar Venda",
)

list_vendas = _views["list"]
create_venda = _views["create"]
update_venda = _views["update"]
