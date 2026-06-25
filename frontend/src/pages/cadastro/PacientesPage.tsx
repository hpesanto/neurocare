import { useState } from "react";
import DataTable from "../../components/DataTable";
import FormModal from "../../components/FormModal";
import { useCrud } from "../../hooks/useCrud";
import { ENDPOINTS } from "../../api/endpoints";
import type { Paciente } from "../../types/models";

export default function PacientesPage() {
  const { items, isLoading, create, update, remove } = useCrud<Paciente>(ENDPOINTS.pacientes);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<Paciente | null>(null);

  const handleSubmit = async (data: Record<string, string>) => {
    if (editing) {
      await update({ id: editing.id, ...data } as unknown as Paciente);
    } else {
      await create(data as unknown as Paciente);
    }
  };

  return (
    <>
      <DataTable
        title="Pacientes"
        columns={[
          { key: "nome_completo", label: "Nome" },
          { key: "cpf", label: "CPF" },
          { key: "telefone_principal", label: "Telefone" },
          { key: "email", label: "Email" },
          { key: "status_paciente", label: "Status" },
          { key: "convenio_nome", label: "Convênio" },
        ]}
        items={items}
        isLoading={isLoading}
        onAdd={() => { setEditing(null); setModalOpen(true); }}
        onEdit={(item) => { setEditing(item); setModalOpen(true); }}
        onDelete={(id) => { if (confirm("Excluir paciente?")) remove(id); }}
      />
      <FormModal
        title={editing ? `Editar ${editing.nome_completo}` : "Novo Paciente"}
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        onSubmit={handleSubmit}
      >
        <div className="form-grid">
          <div className="form-group">
            <label htmlFor="nome_completo">Nome Completo</label>
            <input id="nome_completo" name="nome_completo" defaultValue={editing?.nome_completo ?? ""} required />
          </div>
          <div className="form-group">
            <label htmlFor="cpf">CPF</label>
            <input id="cpf" name="cpf" defaultValue={editing?.cpf ?? ""} />
          </div>
          <div className="form-group">
            <label htmlFor="data_nascimento">Data de Nascimento</label>
            <input id="data_nascimento" name="data_nascimento" type="date" defaultValue={editing?.data_nascimento ?? ""} required />
          </div>
          <div className="form-group">
            <label htmlFor="telefone_principal">Telefone</label>
            <input id="telefone_principal" name="telefone_principal" defaultValue={editing?.telefone_principal ?? ""} required />
          </div>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input id="email" name="email" type="email" defaultValue={editing?.email ?? ""} />
          </div>
          <div className="form-group">
            <label htmlFor="genero">Gênero</label>
            <select id="genero" name="genero" defaultValue={editing?.genero ?? ""}>
              <option value="">Selecione</option>
              <option value="Masculino">Masculino</option>
              <option value="Feminino">Feminino</option>
              <option value="Outro">Outro</option>
              <option value="Não Informar">Não Informar</option>
            </select>
          </div>
          <div className="form-group">
            <label htmlFor="status_paciente">Status</label>
            <select id="status_paciente" name="status_paciente" defaultValue={editing?.status_paciente ?? "Ativo"}>
              <option value="Ativo">Ativo</option>
              <option value="Inativo">Inativo</option>
              <option value="Alta">Alta</option>
              <option value="Em Espera">Em Espera</option>
            </select>
          </div>
        </div>
      </FormModal>
    </>
  );
}
