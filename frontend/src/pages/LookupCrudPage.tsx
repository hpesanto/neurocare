import { useState } from "react";
import DataTable from "../components/DataTable";
import FormModal from "../components/FormModal";
import { useCrud } from "../hooks/useCrud";
import type { LookupItem } from "../types/models";

interface LookupCrudPageProps {
  endpoint: string;
  title: string;
  itemLabel: string;
}

export default function LookupCrudPage({ endpoint, title, itemLabel }: LookupCrudPageProps) {
  const { items, isLoading, create, update, remove } = useCrud<LookupItem>(endpoint);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<LookupItem | null>(null);

  const handleSubmit = async (data: Record<string, string>) => {
    if (editing) {
      await update({ id: editing.id, nome: data.nome } as LookupItem);
    } else {
      await create({ nome: data.nome } as LookupItem);
    }
  };

  return (
    <>
      <DataTable
        title={title}
        columns={[{ key: "nome", label: "Nome" }]}
        items={items}
        isLoading={isLoading}
        onAdd={() => {
          setEditing(null);
          setModalOpen(true);
        }}
        onEdit={(item) => {
          setEditing(item);
          setModalOpen(true);
        }}
        onDelete={(id) => {
          if (confirm(`Excluir ${itemLabel}?`)) remove(id);
        }}
      />
      <FormModal
        title={editing ? `Editar ${itemLabel}` : `Novo ${itemLabel}`}
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        onSubmit={handleSubmit}
      >
        <div className="form-group">
          <label htmlFor="nome">Nome</label>
          <input
            id="nome"
            name="nome"
            type="text"
            defaultValue={editing?.nome ?? ""}
            required
          />
        </div>
      </FormModal>
    </>
  );
}
