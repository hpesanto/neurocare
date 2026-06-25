import { useState } from "react";
import DataTable from "../../components/DataTable";
import FormModal from "../../components/FormModal";
import { useCrud } from "../../hooks/useCrud";
import { ENDPOINTS } from "../../api/endpoints";

interface VendaGeral {
  id: string;
  data_venda: string;
  nome_comprador: string | null;
  contato_comprador: string | null;
  valor_total_transacao: string;
}

export default function VendasGeralPage() {
  const { items, isLoading, create, update, remove } = useCrud<VendaGeral>(ENDPOINTS.vendasGeral);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<VendaGeral | null>(null);

  const handleSubmit = async (data: Record<string, string>) => {
    const cleaned: Record<string, string | null> = {};
    for (const [k, v] of Object.entries(data)) {
      cleaned[k] = v === "" ? null : v;
    }
    if (editing) {
      await update({ id: editing.id, ...cleaned } as unknown as VendaGeral);
    } else {
      await create(cleaned as unknown as VendaGeral);
    }
  };

  return (
    <>
      <DataTable
        title="Vendas Gerais"
        columns={[
          { key: "data_venda", label: "Data" },
          { key: "nome_comprador", label: "Comprador" },
          { key: "contato_comprador", label: "Contato" },
          { key: "valor_total_transacao", label: "Total (R$)" },
        ]}
        items={items}
        isLoading={isLoading}
        onAdd={() => { setEditing(null); setModalOpen(true); }}
        onEdit={(item) => { setEditing(item); setModalOpen(true); }}
        onDelete={(id) => { if (confirm("Excluir venda?")) remove(id); }}
      />
      <FormModal
        title={editing ? "Editar Venda" : "Nova Venda Geral"}
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        onSubmit={handleSubmit}
      >
        <div className="form-grid">
          <div className="form-group">
            <label htmlFor="data_venda">Data</label>
            <input id="data_venda" name="data_venda" type="date" defaultValue={editing?.data_venda ?? ""} required />
          </div>
          <div className="form-group">
            <label htmlFor="valor_total_transacao">Valor Total</label>
            <input id="valor_total_transacao" name="valor_total_transacao" type="number" step="0.01" defaultValue={editing?.valor_total_transacao ?? ""} required />
          </div>
          <div className="form-group">
            <label htmlFor="nome_comprador">Comprador</label>
            <input id="nome_comprador" name="nome_comprador" defaultValue={editing?.nome_comprador ?? ""} />
          </div>
          <div className="form-group">
            <label htmlFor="contato_comprador">Contato</label>
            <input id="contato_comprador" name="contato_comprador" defaultValue={editing?.contato_comprador ?? ""} />
          </div>
        </div>
      </FormModal>
    </>
  );
}
