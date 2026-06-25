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
    const cleaned: Record<string, string | null> = {};
    for (const [k, v] of Object.entries(data)) {
      cleaned[k] = v === "" ? null : v;
    }
    if (editing) {
      await update({ id: editing.id, ...cleaned } as unknown as Paciente);
    } else {
      await create(cleaned as unknown as Paciente);
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
          { key: "genero", label: "Genero" },
          { key: "status_paciente", label: "Status" },
          { key: "convenio_nome", label: "Convenio" },
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
        <h4 style={{ marginBottom: "0.75rem", color: "#64748b", fontSize: "0.8rem", textTransform: "uppercase" }}>Dados Pessoais</h4>
        <div className="form-grid">
          <div className="form-group">
            <label htmlFor="nome_completo">Nome Completo *</label>
            <input id="nome_completo" name="nome_completo" defaultValue={editing?.nome_completo ?? ""} required />
          </div>
          <div className="form-group">
            <label htmlFor="data_nascimento">Data de Nascimento *</label>
            <input id="data_nascimento" name="data_nascimento" type="date" defaultValue={editing?.data_nascimento ?? ""} required />
          </div>
          <div className="form-group">
            <label htmlFor="cpf">CPF</label>
            <input id="cpf" name="cpf" defaultValue={editing?.cpf ?? ""} />
          </div>
          <div className="form-group">
            <label htmlFor="rg">RG</label>
            <input id="rg" name="rg" defaultValue={editing?.rg ?? ""} />
          </div>
          <div className="form-group">
            <label htmlFor="genero">Genero</label>
            <select id="genero" name="genero" defaultValue={editing?.genero ?? ""}>
              <option value="">Selecione</option>
              <option value="Masculino">Masculino</option>
              <option value="Feminino">Feminino</option>
              <option value="Outro">Outro</option>
            </select>
          </div>
          <div className="form-group">
            <label htmlFor="estado_civil">Estado Civil</label>
            <select id="estado_civil" name="estado_civil" defaultValue={editing?.estado_civil ?? ""}>
              <option value="">Selecione</option>
              <option value="Solteiro">Solteiro</option>
              <option value="Casado">Casado</option>
              <option value="Divorciado">Divorciado</option>
            </select>
          </div>
          <div className="form-group">
            <label htmlFor="profissao">Profissao</label>
            <input id="profissao" name="profissao" defaultValue={editing?.profissao ?? ""} />
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

        <h4 style={{ margin: "1rem 0 0.75rem", color: "#64748b", fontSize: "0.8rem", textTransform: "uppercase" }}>Contato</h4>
        <div className="form-grid">
          <div className="form-group">
            <label htmlFor="telefone_principal">Telefone Principal *</label>
            <input id="telefone_principal" name="telefone_principal" defaultValue={editing?.telefone_principal ?? ""} required />
          </div>
          <div className="form-group">
            <label htmlFor="telefone_secundario">Telefone Secundario</label>
            <input id="telefone_secundario" name="telefone_secundario" defaultValue={editing?.telefone_secundario ?? ""} />
          </div>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input id="email" name="email" type="email" defaultValue={editing?.email ?? ""} />
          </div>
        </div>

        <h4 style={{ margin: "1rem 0 0.75rem", color: "#64748b", fontSize: "0.8rem", textTransform: "uppercase" }}>Endereco</h4>
        <div className="form-grid">
          <div className="form-group">
            <label htmlFor="endereco_rua">Rua</label>
            <input id="endereco_rua" name="endereco_rua" defaultValue={editing?.endereco_rua ?? ""} />
          </div>
          <div className="form-group">
            <label htmlFor="endereco_numero">Numero</label>
            <input id="endereco_numero" name="endereco_numero" defaultValue={editing?.endereco_numero ?? ""} />
          </div>
          <div className="form-group">
            <label htmlFor="endereco_complemento">Complemento</label>
            <input id="endereco_complemento" name="endereco_complemento" defaultValue={editing?.endereco_complemento ?? ""} />
          </div>
          <div className="form-group">
            <label htmlFor="endereco_bairro">Bairro</label>
            <input id="endereco_bairro" name="endereco_bairro" defaultValue={editing?.endereco_bairro ?? ""} />
          </div>
          <div className="form-group">
            <label htmlFor="endereco_cidade">Cidade</label>
            <input id="endereco_cidade" name="endereco_cidade" defaultValue={editing?.endereco_cidade ?? ""} />
          </div>
          <div className="form-group">
            <label htmlFor="endereco_estado">Estado</label>
            <input id="endereco_estado" name="endereco_estado" defaultValue={editing?.endereco_estado ?? ""} />
          </div>
          <div className="form-group">
            <label htmlFor="endereco_cep">CEP</label>
            <input id="endereco_cep" name="endereco_cep" defaultValue={editing?.endereco_cep ?? ""} />
          </div>
        </div>

        <h4 style={{ margin: "1rem 0 0.75rem", color: "#64748b", fontSize: "0.8rem", textTransform: "uppercase" }}>Encaminhamento e Convenio</h4>
        <div className="form-grid">
          <div className="form-group">
            <label htmlFor="quem_encaminhou">Quem Encaminhou</label>
            <input id="quem_encaminhou" name="quem_encaminhou" defaultValue={editing?.quem_encaminhou ?? ""} />
          </div>
          <div className="form-group">
            <label htmlFor="numero_carteirinha_convenio">N. Carteirinha Convenio</label>
            <input id="numero_carteirinha_convenio" name="numero_carteirinha_convenio" defaultValue={editing?.numero_carteirinha_convenio ?? ""} />
          </div>
          <div className="form-group">
            <label htmlFor="validade_carteirinha_convenio">Validade Carteirinha</label>
            <input id="validade_carteirinha_convenio" name="validade_carteirinha_convenio" type="date" defaultValue={editing?.validade_carteirinha_convenio ?? ""} />
          </div>
        </div>
        <div className="form-group">
          <label htmlFor="motivo_encaminhamento">Motivo do Encaminhamento</label>
          <textarea id="motivo_encaminhamento" name="motivo_encaminhamento" rows={3} defaultValue={editing?.motivo_encaminhamento ?? ""} />
        </div>
        <div className="form-group">
          <label htmlFor="observacoes_gerais">Observacoes Gerais</label>
          <textarea id="observacoes_gerais" name="observacoes_gerais" rows={3} defaultValue={editing?.observacoes_gerais ?? ""} />
        </div>
      </FormModal>
    </>
  );
}
