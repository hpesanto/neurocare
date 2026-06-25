import { useState } from "react";
import DataTable from "../../components/DataTable";
import FormModal from "../../components/FormModal";
import { useCrud } from "../../hooks/useCrud";
import { ENDPOINTS } from "../../api/endpoints";
import type { EvolucaoClinica } from "../../types/models";

export default function EvolucaoClinicaPage() {
  const { items, isLoading, create, update, remove } = useCrud<EvolucaoClinica>(ENDPOINTS.evolucaoClinica);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<EvolucaoClinica | null>(null);

  const handleSubmit = async (data: Record<string, string>) => {
    const cleaned: Record<string, string | null> = {};
    for (const [k, v] of Object.entries(data)) {
      cleaned[k] = v === "" ? null : v;
    }
    if (editing) {
      await update({ id: editing.id, ...cleaned } as unknown as EvolucaoClinica);
    } else {
      await create(cleaned as unknown as EvolucaoClinica);
    }
  };

  return (
    <>
      <DataTable
        title="Evolucao Clinica"
        columns={[
          { key: "paciente_nome", label: "Paciente" },
          { key: "psicologo_nome", label: "Psicologo" },
          { key: "data_sessao", label: "Data" },
          { key: "hora_sessao", label: "Hora" },
        ]}
        items={items}
        isLoading={isLoading}
        onAdd={() => { setEditing(null); setModalOpen(true); }}
        onEdit={(item) => { setEditing(item); setModalOpen(true); }}
        onDelete={(id) => { if (confirm("Excluir evolucao?")) remove(id); }}
      />
      <FormModal
        title={editing ? "Editar Evolucao" : "Nova Evolucao Clinica"}
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        onSubmit={handleSubmit}
      >
        <div className="form-grid">
          <div className="form-group">
            <label htmlFor="id_paciente">ID Paciente</label>
            <input id="id_paciente" name="id_paciente" defaultValue={editing?.id_paciente ?? ""} required />
          </div>
          <div className="form-group">
            <label htmlFor="id_psicologo">ID Psicologo</label>
            <input id="id_psicologo" name="id_psicologo" defaultValue={editing?.id_psicologo ?? ""} required />
          </div>
          <div className="form-group">
            <label htmlFor="data_sessao">Data</label>
            <input id="data_sessao" name="data_sessao" type="date" defaultValue={editing?.data_sessao ?? ""} required />
          </div>
          <div className="form-group">
            <label htmlFor="hora_sessao">Hora</label>
            <input id="hora_sessao" name="hora_sessao" type="time" defaultValue={editing?.hora_sessao ?? ""} />
          </div>
        </div>
        <div className="form-group">
          <label htmlFor="evolucao_texto">Evolucao</label>
          <textarea id="evolucao_texto" name="evolucao_texto" rows={5} defaultValue={editing?.evolucao_texto ?? ""} required />
        </div>
      </FormModal>
    </>
  );
}
