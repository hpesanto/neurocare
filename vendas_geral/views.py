from neurocare_project.crud_views import make_crud_views

from .forms import VendaGeralForm, VendaGeralItemForm
from .models import VendaGeral, VendaGeralItem

_venda_views = make_crud_views(
    model=VendaGeral,
    form_class=VendaGeralForm,
    list_template="vendas_geral/list.html",
    row_template="vendas_geral/row.html",
    form_template="vendas_geral/form.html",
    form_partial_template="vendas_geral/_form_partial.html",
    list_url_name="vendas_geral:list",
    list_order_by=["-data_venda"],
    create_title="Nova Venda (Geral)",
    edit_title_fn=lambda i: "Editar Venda (Geral)",
)

_item_views = make_crud_views(
    model=VendaGeralItem,
    form_class=VendaGeralItemForm,
    list_template="vendas_geral/itens_list.html",
    row_template="vendas_geral/itens_row.html",
    form_template="vendas_geral/itens_form.html",
    form_partial_template="vendas_geral/itens_form_partial.html",
    list_url_name="vendas_geral:itens_list",
    list_order_by=["-data_criacao"],
    create_title="Novo Item de Venda",
    edit_title_fn=lambda i: "Editar Item de Venda",
)

list_venda_geral = _venda_views["list"]
create_venda_geral = _venda_views["create"]
update_venda_geral = _venda_views["update"]

list_venda_geral_itens = _item_views["list"]
create_venda_geral_item = _item_views["create"]
update_venda_geral_item = _item_views["update"]
