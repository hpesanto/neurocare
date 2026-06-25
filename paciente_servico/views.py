from neurocare_project.crud_views import make_crud_views
from pacientes.models import PacienteServico

from .forms import PacienteServicoForm

_views = make_crud_views(
    model=PacienteServico,
    form_class=PacienteServicoForm,
    list_template="paciente_servico/list.html",
    row_template="paciente_servico/row.html",
    form_template="paciente_servico/form.html",
    form_partial_template="paciente_servico/_form_partial.html",
    list_url_name="paciente_servico:list",
    list_order_by=["-id"],
    create_title="Novo Serviço do Paciente",
    edit_title_fn=lambda i: "Editar Serviço do Paciente",
    item_context_name="servico",
    list_context_name="servicos",
)

list_paciente_servicos = _views["list"]
create_paciente_servico = _views["create"]
update_paciente_servico = _views["update"]
