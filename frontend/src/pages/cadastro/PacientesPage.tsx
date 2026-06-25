import { useState } from "react";
import { Col, Form, Row } from "react-bootstrap";
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
        size="xl"
      >
        <h6 className="text-muted text-uppercase small fw-bold mb-3">
          <i className="bi bi-person me-1" /> Dados Pessoais
        </h6>
        <Row className="g-3 mb-4">
          <Col md={6}>
            <Form.Group>
              <Form.Label>Nome Completo *</Form.Label>
              <Form.Control name="nome_completo" defaultValue={editing?.nome_completo ?? ""} required />
            </Form.Group>
          </Col>
          <Col md={3}>
            <Form.Group>
              <Form.Label>Data Nascimento *</Form.Label>
              <Form.Control name="data_nascimento" type="date" defaultValue={editing?.data_nascimento ?? ""} required />
            </Form.Group>
          </Col>
          <Col md={3}>
            <Form.Group>
              <Form.Label>CPF</Form.Label>
              <Form.Control name="cpf" defaultValue={editing?.cpf ?? ""} />
            </Form.Group>
          </Col>
          <Col md={3}>
            <Form.Group>
              <Form.Label>RG</Form.Label>
              <Form.Control name="rg" defaultValue={editing?.rg ?? ""} />
            </Form.Group>
          </Col>
          <Col md={3}>
            <Form.Group>
              <Form.Label>Genero</Form.Label>
              <Form.Select name="genero" defaultValue={editing?.genero ?? ""}>
                <option value="">Selecione</option>
                <option value="Masculino">Masculino</option>
                <option value="Feminino">Feminino</option>
                <option value="Outro">Outro</option>
              </Form.Select>
            </Form.Group>
          </Col>
          <Col md={3}>
            <Form.Group>
              <Form.Label>Estado Civil</Form.Label>
              <Form.Select name="estado_civil" defaultValue={editing?.estado_civil ?? ""}>
                <option value="">Selecione</option>
                <option value="Solteiro">Solteiro</option>
                <option value="Casado">Casado</option>
                <option value="Divorciado">Divorciado</option>
              </Form.Select>
            </Form.Group>
          </Col>
          <Col md={3}>
            <Form.Group>
              <Form.Label>Profissao</Form.Label>
              <Form.Control name="profissao" defaultValue={editing?.profissao ?? ""} />
            </Form.Group>
          </Col>
          <Col md={3}>
            <Form.Group>
              <Form.Label>Status</Form.Label>
              <Form.Select name="status_paciente" defaultValue={editing?.status_paciente ?? "Ativo"}>
                <option value="Ativo">Ativo</option>
                <option value="Inativo">Inativo</option>
                <option value="Alta">Alta</option>
                <option value="Em Espera">Em Espera</option>
              </Form.Select>
            </Form.Group>
          </Col>
        </Row>

        <h6 className="text-muted text-uppercase small fw-bold mb-3">
          <i className="bi bi-telephone me-1" /> Contato
        </h6>
        <Row className="g-3 mb-4">
          <Col md={4}>
            <Form.Group>
              <Form.Label>Telefone Principal *</Form.Label>
              <Form.Control name="telefone_principal" defaultValue={editing?.telefone_principal ?? ""} required />
            </Form.Group>
          </Col>
          <Col md={4}>
            <Form.Group>
              <Form.Label>Telefone Secundario</Form.Label>
              <Form.Control name="telefone_secundario" defaultValue={editing?.telefone_secundario ?? ""} />
            </Form.Group>
          </Col>
          <Col md={4}>
            <Form.Group>
              <Form.Label>Email</Form.Label>
              <Form.Control name="email" type="email" defaultValue={editing?.email ?? ""} />
            </Form.Group>
          </Col>
        </Row>

        <h6 className="text-muted text-uppercase small fw-bold mb-3">
          <i className="bi bi-geo-alt me-1" /> Endereco
        </h6>
        <Row className="g-3 mb-4">
          <Col md={5}>
            <Form.Group>
              <Form.Label>Rua</Form.Label>
              <Form.Control name="endereco_rua" defaultValue={editing?.endereco_rua ?? ""} />
            </Form.Group>
          </Col>
          <Col md={2}>
            <Form.Group>
              <Form.Label>Numero</Form.Label>
              <Form.Control name="endereco_numero" defaultValue={editing?.endereco_numero ?? ""} />
            </Form.Group>
          </Col>
          <Col md={2}>
            <Form.Group>
              <Form.Label>Complemento</Form.Label>
              <Form.Control name="endereco_complemento" defaultValue={editing?.endereco_complemento ?? ""} />
            </Form.Group>
          </Col>
          <Col md={3}>
            <Form.Group>
              <Form.Label>Bairro</Form.Label>
              <Form.Control name="endereco_bairro" defaultValue={editing?.endereco_bairro ?? ""} />
            </Form.Group>
          </Col>
          <Col md={4}>
            <Form.Group>
              <Form.Label>Cidade</Form.Label>
              <Form.Control name="endereco_cidade" defaultValue={editing?.endereco_cidade ?? ""} />
            </Form.Group>
          </Col>
          <Col md={4}>
            <Form.Group>
              <Form.Label>Estado</Form.Label>
              <Form.Control name="endereco_estado" defaultValue={editing?.endereco_estado ?? ""} />
            </Form.Group>
          </Col>
          <Col md={4}>
            <Form.Group>
              <Form.Label>CEP</Form.Label>
              <Form.Control name="endereco_cep" defaultValue={editing?.endereco_cep ?? ""} />
            </Form.Group>
          </Col>
        </Row>

        <h6 className="text-muted text-uppercase small fw-bold mb-3">
          <i className="bi bi-send me-1" /> Encaminhamento e Convenio
        </h6>
        <Row className="g-3 mb-3">
          <Col md={4}>
            <Form.Group>
              <Form.Label>Quem Encaminhou</Form.Label>
              <Form.Control name="quem_encaminhou" defaultValue={editing?.quem_encaminhou ?? ""} />
            </Form.Group>
          </Col>
          <Col md={4}>
            <Form.Group>
              <Form.Label>N. Carteirinha</Form.Label>
              <Form.Control name="numero_carteirinha_convenio" defaultValue={editing?.numero_carteirinha_convenio ?? ""} />
            </Form.Group>
          </Col>
          <Col md={4}>
            <Form.Group>
              <Form.Label>Validade Carteirinha</Form.Label>
              <Form.Control name="validade_carteirinha_convenio" type="date" defaultValue={editing?.validade_carteirinha_convenio ?? ""} />
            </Form.Group>
          </Col>
          <Col md={6}>
            <Form.Group>
              <Form.Label>Motivo Encaminhamento</Form.Label>
              <Form.Control as="textarea" rows={2} name="motivo_encaminhamento" defaultValue={editing?.motivo_encaminhamento ?? ""} />
            </Form.Group>
          </Col>
          <Col md={6}>
            <Form.Group>
              <Form.Label>Observacoes Gerais</Form.Label>
              <Form.Control as="textarea" rows={2} name="observacoes_gerais" defaultValue={editing?.observacoes_gerais ?? ""} />
            </Form.Group>
          </Col>
        </Row>
      </FormModal>
    </>
  );
}
