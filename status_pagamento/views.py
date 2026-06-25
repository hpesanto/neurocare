from neurocare_project.crud_views import make_crud_views

from .forms import StatusPagamentoForm
from .models import StatusPagamento

_views = make_crud_views(
    model=StatusPagamento,
    form_class=StatusPagamentoForm,
    list_template="status_pagamento/list.html",
    row_template="status_pagamento/row.html",
    form_template="status_pagamento/form.html",
    form_partial_template="status_pagamento/_form_partial.html",
    list_url_name="status_pagamento:list",
    list_order_by=["nome"],
    create_title="Novo Status de Pagamento",
    edit_title_fn=lambda i: "Editar Status",
    enable_delete=True,
)

list_status_pagamento = _views["list"]
create_status = _views["create"]
update_status = _views["update"]
delete_status = _views["delete"]
