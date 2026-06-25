from neurocare_project.crud_views import make_crud_views
from pacientes.models import TipoServico

from .forms import TipoServicoForm

_views = make_crud_views(
    model=TipoServico,
    form_class=TipoServicoForm,
    list_template="tipos_servico/list.html",
    row_template="tipos_servico/row.html",
    form_template="tipos_servico/form.html",
    form_partial_template="tipos_servico/_form_partial.html",
    list_url_name="tipos_servico:list",
    list_order_by=["nome"],
    create_title="Novo Tipo de Serviço",
    edit_title_fn=lambda i: f"Editar {i.nome}",
    item_context_name="tipo",
    list_context_name="tipos",
)

list_tipos_servico = _views["list"]
create_tipo_servico = _views["create"]
update_tipo_servico = _views["update"]
