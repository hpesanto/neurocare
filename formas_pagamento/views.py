from neurocare_project.crud_views import make_crud_views
from pacientes.models import FormaPagamento

from .forms import FormaPagamentoForm

_views = make_crud_views(
    model=FormaPagamento,
    form_class=FormaPagamentoForm,
    list_template="formas_pagamento/list.html",
    row_template="formas_pagamento/row.html",
    form_template="formas_pagamento/form.html",
    form_partial_template="formas_pagamento/_form_partial.html",
    list_url_name="formas_pagamento:list",
    list_order_by=["nome"],
    create_title="Nova Forma de Pagamento",
    edit_title_fn=lambda i: f"Editar {i.nome}",
    item_context_name="forma",
    list_context_name="formas",
)

list_formas = _views["list"]
create_forma = _views["create"]
update_forma = _views["update"]
