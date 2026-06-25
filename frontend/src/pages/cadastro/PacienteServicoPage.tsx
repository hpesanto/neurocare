import { useState } from "react";
import { Col, Form, Row } from "react-bootstrap";
import DataTable from "../../components/DataTable";
import FormModal from "../../components/FormModal";
import FkSelect from "../../components/FkSelect";
import { useCrud } from "../../hooks/useCrud";
import { ENDPOINTS } from "../../api/endpoints";

interface PacienteServico {
  id: string;
  id_paciente: string;
  paciente_nome: string | null;
  id_tipo_servico: string;
  servico_nome: string | null;
  data_inicio: string;
  data_fim: string | null;
  ativo: boolean;
  observacoes: string | null;
}

export default function PacienteServicoPage() {
  const { items, isLoading, create, update, remove } = useCrud<PacienteServico>(ENDPOINTS.pacienteServico);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<PacienteServico | null>(null);

  const handleSubmit = async (data: Record<string, string>) => {
    const cleaned: Record<string, string | null> = {};
    for (const [k, v] of Object.entries(data)) {
      cleaned[k] = v === "" ? null : v;
    }
    if (editing) {
      await update({ id: editing.id, ...cleaned } as unknown as PacienteServico);
    } else {
      await create(cleaned as unknown as PacienteServico);
    }
  };

  return (
    <>
      <DataTable
        title="Servicos do Paciente"
        columns={[
          { key: "paciente_nome", label: "Paciente" },
          { key: "servico_nome", label: "Servico" },
          { key: "data_inicio", label: "Inicio" },
          { key: "data_fim", label: "Fim" },
          { key: "ativo", label: "Ativo", render: (i) => (i.ativo ? "Sim" : "Nao") },
        ]}
        items={items}
        isLoading={isLoading}
        onAdd={() => { setEditing(null); setModalOpen(true); }}
        onEdit={(item) => { setEditing(item); setModalOpen(true); }}
        onDelete={(id) => { if (confirm("Excluir servico?")) remove(id); }}
      />
      <FormModal
        title={editing ? "Editar Servico" : "Novo Servico do Paciente"}
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        onSubmit={handleSubmit}
      >
        <Row className="g-3">
          <Col md={6}>
            <FkSelect name="id_paciente" label="Paciente" endpoint={ENDPOINTS.pacientes} labelField="nome_completo" defaultValue={editing?.id_paciente} required />
          </Col>
          <Col md={6}>
            <FkSelect name="id_tipo_servico" label="Tipo de Servico" endpoint={ENDPOINTS.tiposServico} defaultValue={editing?.id_tipo_servico} required />
          </Col>
          <Col md={4}>
            <Form.Group>
              <Form.Label>Data Inicio</Form.Label>
              <Form.Control name="data_inicio" type="date" defaultValue={editing?.data_inicio ?? ""} />
            </Form.Group>
          </Col>
          <Col md={4}>
            <Form.Group>
              <Form.Label>Data Fim</Form.Label>
              <Form.Control name="data_fim" type="date" defaultValue={editing?.data_fim ?? ""} />
            </Form.Group>
          </Col>
          <Col md={12}>
            <Form.Group>
              <Form.Label>Observacoes</Form.Label>
              <Form.Control as="textarea" rows={2} name="observacoes" defaultValue={editing?.observacoes ?? ""} />
            </Form.Group>
          </Col>
        </Row>
      </FormModal>
    </>
  );
}
