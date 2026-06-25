from neurocare_project.crud_views import make_crud_views

from .forms import EvolucaoClinicaForm
from .models import EvolucaoClinica

_views = make_crud_views(
    model=EvolucaoClinica,
    form_class=EvolucaoClinicaForm,
    list_template="evolucao_clinica/list.html",
    row_template="evolucao_clinica/row.html",
    form_template="evolucao_clinica/form.html",
    form_partial_template="evolucao_clinica/_form_partial.html",
    list_url_name="evolucao:list",
    list_order_by=["-data_sessao", "-hora_sessao"],
    create_title="Nova Evolução Clínica",
    edit_title_fn=lambda i: "Editar Evolução",
)

list_evolucao = _views["list"]
create_evolucao = _views["create"]
update_evolucao = _views["update"]
