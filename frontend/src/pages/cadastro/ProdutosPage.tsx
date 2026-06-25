import { useState } from "react";
import DataTable from "../../components/DataTable";
import FormModal from "../../components/FormModal";
import { useCrud } from "../../hooks/useCrud";
import { ENDPOINTS } from "../../api/endpoints";

interface Produto {
  id: string;
  nome: string;
  descricao: string | null;
  valor_unitario: string;
  ativo: boolean;
  tipo_produto_nome: string | null;
  id_tipo_produto: string | null;
}

export default function ProdutosPage() {
  const { items, isLoading, create, update, remove } = useCrud<Produto>(ENDPOINTS.produtos);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<Produto | null>(null);

  const handleSubmit = async (data: Record<string, string>) => {
    const cleaned: Record<string, string | null> = {};
    for (const [k, v] of Object.entries(data)) {
      cleaned[k] = v === "" ? null : v;
    }
    if (editing) {
      await update({ id: editing.id, ...cleaned } as unknown as Produto);
    } else {
      await create(cleaned as unknown as Produto);
    }
  };

  return (
    <>
      <DataTable
        title="Produtos"
        columns={[
          { key: "nome", label: "Nome" },
          { key: "tipo_produto_nome", label: "Tipo" },
          { key: "valor_unitario", label: "Valor (R$)" },
          { key: "ativo", label: "Ativo", render: (i) => (i.ativo ? "Sim" : "Não") },
        ]}
        items={items}
        isLoading={isLoading}
        onAdd={() => { setEditing(null); setModalOpen(true); }}
        onEdit={(item) => { setEditing(item); setModalOpen(true); }}
        onDelete={(id) => { if (confirm("Excluir produto?")) remove(id); }}
      />
      <FormModal
        title={editing ? `Editar ${editing.nome}` : "Novo Produto"}
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        onSubmit={handleSubmit}
      >
        <div className="form-grid">
          <div className="form-group">
            <label htmlFor="nome">Nome</label>
            <input id="nome" name="nome" defaultValue={editing?.nome ?? ""} required />
          </div>
          <div className="form-group">
            <label htmlFor="valor_unitario">Valor Unitario</label>
            <input id="valor_unitario" name="valor_unitario" type="number" step="0.01" defaultValue={editing?.valor_unitario ?? ""} required />
          </div>
          <div className="form-group">
            <label htmlFor="descricao">Descricao</label>
            <textarea id="descricao" name="descricao" defaultValue={editing?.descricao ?? ""} />
          </div>
        </div>
      </FormModal>
    </>
  );
}
