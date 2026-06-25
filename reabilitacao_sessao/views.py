from neurocare_project.crud_views import make_crud_views

from .forms import ReabilitacaoSessaoForm
from .models import ReabilitacaoSessao

_views = make_crud_views(
    model=ReabilitacaoSessao,
    form_class=ReabilitacaoSessaoForm,
    list_template="reabilitacao_sessao/list.html",
    row_template="reabilitacao_sessao/row.html",
    form_template="reabilitacao_sessao/form.html",
    form_partial_template="reabilitacao_sessao/_form_partial.html",
    list_url_name="sessoes:list",
    list_order_by=["-data_sessao", "-hora_sessao"],
    create_title="Nova Sessão de Reabilitação",
    edit_title_fn=lambda i: "Editar Sessão",
)

list_sessoes = _views["list"]
create_sessao = _views["create"]
update_sessao = _views["update"]
