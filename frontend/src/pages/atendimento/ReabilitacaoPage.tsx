import { useState } from "react";
import DataTable from "../../components/DataTable";
import FormModal from "../../components/FormModal";
import { useCrud } from "../../hooks/useCrud";
import { ENDPOINTS } from "../../api/endpoints";

interface Reabilitacao {
  id: string;
  id_paciente: string;
  paciente_nome: string | null;
  psicologo_nome: string | null;
  data_inicio: string;
  data_fim_prevista: string | null;
  programa_descricao: string;
  num_sessoes_planejadas: number | null;
  frequencia: string | null;
}

export default function ReabilitacaoPage() {
  const { items, isLoading, create, update, remove } = useCrud<Reabilitacao>(ENDPOINTS.reabilitacaoNeuropsicologica);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<Reabilitacao | null>(null);

  const handleSubmit = async (data: Record<string, string>) => {
    const cleaned: Record<string, string | null> = {};
    for (const [k, v] of Object.entries(data)) {
      cleaned[k] = v === "" ? null : v;
    }
    if (editing) {
      await update({ id: editing.id, ...cleaned } as unknown as Reabilitacao);
    } else {
      await create(cleaned as unknown as Reabilitacao);
    }
  };

  return (
    <>
      <DataTable
        title="Reabilitacao Neuropsicologica"
        columns={[
          { key: "paciente_nome", label: "Paciente" },
          { key: "psicologo_nome", label: "Psicologo" },
          { key: "data_inicio", label: "Inicio" },
          { key: "data_fim_prevista", label: "Fim Previsto" },
          { key: "frequencia", label: "Frequencia" },
        ]}
        items={items}
        isLoading={isLoading}
        onAdd={() => { setEditing(null); setModalOpen(true); }}
        onEdit={(item) => { setEditing(item); setModalOpen(true); }}
        onDelete={(id) => { if (confirm("Excluir reabilitacao?")) remove(id); }}
      />
      <FormModal
        title={editing ? "Editar Reabilitacao" : "Nova Reabilitacao"}
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
            <label htmlFor="data_inicio">Data Inicio</label>
            <input id="data_inicio" name="data_inicio" type="date" defaultValue={editing?.data_inicio ?? ""} required />
          </div>
          <div className="form-group">
            <label htmlFor="data_fim_prevista">Fim Previsto</label>
            <input id="data_fim_prevista" name="data_fim_prevista" type="date" defaultValue={editing?.data_fim_prevista ?? ""} />
          </div>
          <div className="form-group">
            <label htmlFor="frequencia">Frequencia</label>
            <input id="frequencia" name="frequencia" defaultValue={editing?.frequencia ?? ""} />
          </div>
        </div>
        <div className="form-group">
          <label htmlFor="programa_descricao">Descricao do Programa</label>
          <textarea id="programa_descricao" name="programa_descricao" rows={4} defaultValue={editing?.programa_descricao ?? ""} required />
        </div>
      </FormModal>
    </>
  );
}
