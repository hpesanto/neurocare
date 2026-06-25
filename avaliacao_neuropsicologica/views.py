from neurocare_project.crud_views import make_crud_views

from .forms import AvaliacaoNeuropsicologicaForm
from .models import AvaliacaoNeuropsicologica

_views = make_crud_views(
    model=AvaliacaoNeuropsicologica,
    form_class=AvaliacaoNeuropsicologicaForm,
    list_template="avaliacao_neuropsicologica/list.html",
    row_template="avaliacao_neuropsicologica/row.html",
    form_template="avaliacao_neuropsicologica/form.html",
    form_partial_template="avaliacao_neuropsicologica/_form_partial.html",
    list_url_name="avaliacao:list",
    list_order_by=["-data_avaliacao"],
    create_title="Nova Avaliação Neuropsicológica",
    edit_title_fn=lambda i: "Editar Avaliação",
)

list_avaliacao = _views["list"]
create_avaliacao = _views["create"]
update_avaliacao = _views["update"]
