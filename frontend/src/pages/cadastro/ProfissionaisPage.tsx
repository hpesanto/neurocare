import { useState } from "react";
import DataTable from "../../components/DataTable";
import FormModal from "../../components/FormModal";
import { useCrud } from "../../hooks/useCrud";
import { ENDPOINTS } from "../../api/endpoints";
import type { Profissional } from "../../types/models";

export default function ProfissionaisPage() {
  const { items, isLoading, create, update, remove } = useCrud<Profissional>(ENDPOINTS.profissionais);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<Profissional | null>(null);

  const handleSubmit = async (data: Record<string, string>) => {
    const cleaned: Record<string, string | null> = {};
    for (const [k, v] of Object.entries(data)) {
      cleaned[k] = v === "" ? null : v;
    }
    if (editing) {
      await update({ id: editing.id, ...cleaned } as unknown as Profissional);
    } else {
      await create(cleaned as unknown as Profissional);
    }
  };

  return (
    <>
      <DataTable
        title="Profissionais"
        columns={[
          { key: "nome", label: "Nome" },
          { key: "email", label: "Email" },
          { key: "login", label: "Login" },
          { key: "perfil_acesso_nome", label: "Perfil" },
          { key: "ativo", label: "Ativo", render: (i) => (i.ativo ? "Sim" : "Nao") },
        ]}
        items={items}
        isLoading={isLoading}
        onAdd={() => { setEditing(null); setModalOpen(true); }}
        onEdit={(item) => { setEditing(item); setModalOpen(true); }}
        onDelete={(id) => { if (confirm("Excluir profissional?")) remove(id); }}
      />
      <FormModal
        title={editing ? `Editar ${editing.nome}` : "Novo Profissional"}
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        onSubmit={handleSubmit}
      >
        <div className="form-grid">
          <div className="form-group">
            <label htmlFor="nome">Nome *</label>
            <input id="nome" name="nome" defaultValue={editing?.nome ?? ""} required />
          </div>
          <div className="form-group">
            <label htmlFor="email">Email *</label>
            <input id="email" name="email" type="email" defaultValue={editing?.email ?? ""} required />
          </div>
          <div className="form-group">
            <label htmlFor="login">Login *</label>
            <input id="login" name="login" defaultValue={editing?.login ?? ""} required />
          </div>
          <div className="form-group">
            <label htmlFor="senha">{editing ? "Nova Senha" : "Senha *"}</label>
            <input id="senha" name="senha" type="password" required={!editing} />
          </div>
        </div>
      </FormModal>
    </>
  );
}
