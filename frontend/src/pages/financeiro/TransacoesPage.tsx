import { useState } from "react";
import DataTable from "../../components/DataTable";
import FormModal from "../../components/FormModal";
import { useCrud } from "../../hooks/useCrud";
import { ENDPOINTS } from "../../api/endpoints";
import type { TransacaoFinanceira } from "../../types/models";

export default function TransacoesPage() {
  const { items, isLoading, create, update, remove } = useCrud<TransacaoFinanceira>(ENDPOINTS.transacoes);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<TransacaoFinanceira | null>(null);

  const handleSubmit = async (data: Record<string, string>) => {
    const cleaned: Record<string, string | null> = {};
    for (const [k, v] of Object.entries(data)) {
      cleaned[k] = v === "" ? null : v;
    }
    if (editing) {
      await update({ id: editing.id, ...cleaned } as unknown as TransacaoFinanceira);
    } else {
      await create(cleaned as unknown as TransacaoFinanceira);
    }
  };

  return (
    <>
      <DataTable
        title="Transacoes Financeiras"
        columns={[
          { key: "data_transacao", label: "Data" },
          { key: "paciente_nome", label: "Paciente" },
          { key: "tipo_transacao_nome", label: "Tipo" },
          { key: "valor", label: "Valor (R$)" },
          { key: "forma_pagamento_nome", label: "Pagamento" },
          { key: "status_pagamento_nome", label: "Status" },
        ]}
        items={items}
        isLoading={isLoading}
        onAdd={() => { setEditing(null); setModalOpen(true); }}
        onEdit={(item) => { setEditing(item); setModalOpen(true); }}
        onDelete={(id) => { if (confirm("Excluir transacao?")) remove(id); }}
      />
      <FormModal
        title={editing ? "Editar Transacao" : "Nova Transacao"}
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        onSubmit={handleSubmit}
      >
        <div className="form-grid">
          <div className="form-group">
            <label htmlFor="data_transacao">Data</label>
            <input id="data_transacao" name="data_transacao" type="date" defaultValue={editing?.data_transacao ?? ""} required />
          </div>
          <div className="form-group">
            <label htmlFor="valor">Valor</label>
            <input id="valor" name="valor" type="number" step="0.01" defaultValue={editing?.valor ?? ""} required />
          </div>
          <div className="form-group">
            <label htmlFor="id_tipo_transacao">ID Tipo Transacao</label>
            <input id="id_tipo_transacao" name="id_tipo_transacao" defaultValue={editing?.id_tipo_transacao ?? ""} required />
          </div>
          <div className="form-group">
            <label htmlFor="id_forma_pagamento">ID Forma Pagamento</label>
            <input id="id_forma_pagamento" name="id_forma_pagamento" defaultValue={editing?.id_forma_pagamento ?? ""} required />
          </div>
          <div className="form-group">
            <label htmlFor="id_status_pagamento">ID Status Pagamento</label>
            <input id="id_status_pagamento" name="id_status_pagamento" defaultValue={editing?.id_status_pagamento ?? ""} required />
          </div>
        </div>
        <div className="form-group">
          <label htmlFor="descricao">Descricao</label>
          <textarea id="descricao" name="descricao" rows={3} defaultValue={editing?.descricao ?? ""} required />
        </div>
      </FormModal>
    </>
  );
}
