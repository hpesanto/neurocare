import { useState } from "react";
import DataTable from "../../components/DataTable";
import FormModal from "../../components/FormModal";
import { useCrud } from "../../hooks/useCrud";
import { ENDPOINTS } from "../../api/endpoints";

interface ContatoEmergencia {
  id: string;
  id_paciente: string;
  paciente_nome: string | null;
  nome_contato: string;
  telefone_contato: string;
  parentesco: string;
}

export default function ContatosEmergenciaPage() {
  const { items, isLoading, create, update, remove } = useCrud<ContatoEmergencia>(ENDPOINTS.contatosEmergencia);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<ContatoEmergencia | null>(null);

  const handleSubmit = async (data: Record<string, string>) => {
    const cleaned: Record<string, string | null> = {};
    for (const [k, v] of Object.entries(data)) {
      cleaned[k] = v === "" ? null : v;
    }
    if (editing) {
      await update({ id: editing.id, ...cleaned } as unknown as ContatoEmergencia);
    } else {
      await create(cleaned as unknown as ContatoEmergencia);
    }
  };

  return (
    <>
      <DataTable
        title="Contatos de Emergencia"
        columns={[
          { key: "nome_contato", label: "Nome" },
          { key: "telefone_contato", label: "Telefone" },
          { key: "parentesco", label: "Parentesco" },
          { key: "paciente_nome", label: "Paciente" },
        ]}
        items={items}
        isLoading={isLoading}
        onAdd={() => { setEditing(null); setModalOpen(true); }}
        onEdit={(item) => { setEditing(item); setModalOpen(true); }}
        onDelete={(id) => { if (confirm("Excluir contato?")) remove(id); }}
      />
      <FormModal
        title={editing ? "Editar Contato" : "Novo Contato de Emergencia"}
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        onSubmit={handleSubmit}
      >
        <div className="form-grid">
          <div className="form-group">
            <label htmlFor="nome_contato">Nome</label>
            <input id="nome_contato" name="nome_contato" defaultValue={editing?.nome_contato ?? ""} required />
          </div>
          <div className="form-group">
            <label htmlFor="telefone_contato">Telefone</label>
            <input id="telefone_contato" name="telefone_contato" defaultValue={editing?.telefone_contato ?? ""} required />
          </div>
          <div className="form-group">
            <label htmlFor="parentesco">Parentesco</label>
            <input id="parentesco" name="parentesco" defaultValue={editing?.parentesco ?? ""} required />
          </div>
          <div className="form-group">
            <label htmlFor="id_paciente">ID Paciente</label>
            <input id="id_paciente" name="id_paciente" defaultValue={editing?.id_paciente ?? ""} required />
          </div>
        </div>
      </FormModal>
    </>
  );
}
