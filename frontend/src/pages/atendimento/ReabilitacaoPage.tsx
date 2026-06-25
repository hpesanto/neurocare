import { useState } from "react";
import { Col, Form, Row } from "react-bootstrap";
import DataTable from "../../components/DataTable";
import FormModal from "../../components/FormModal";
import FkSelect from "../../components/FkSelect";
import { useCrud } from "../../hooks/useCrud";
import { ENDPOINTS } from "../../api/endpoints";

interface Reabilitacao {
  id: string;
  id_paciente: string;
  id_psicologo: string;
  paciente_nome: string | null;
  psicologo_nome: string | null;
  data_inicio: string;
  data_fim_prevista: string | null;
  programa_descricao: string;
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
        <Row className="g-3">
          <Col md={6}>
            <FkSelect name="id_paciente" label="Paciente" endpoint={ENDPOINTS.pacientes} labelField="nome_completo" defaultValue={editing?.id_paciente} required />
          </Col>
          <Col md={6}>
            <FkSelect name="id_psicologo" label="Psicologo" endpoint={ENDPOINTS.profissionais} labelField="nome" defaultValue={editing?.id_psicologo} required />
          </Col>
          <Col md={4}>
            <Form.Group>
              <Form.Label>Data Inicio *</Form.Label>
              <Form.Control name="data_inicio" type="date" defaultValue={editing?.data_inicio ?? ""} required />
            </Form.Group>
          </Col>
          <Col md={4}>
            <Form.Group>
              <Form.Label>Fim Previsto</Form.Label>
              <Form.Control name="data_fim_prevista" type="date" defaultValue={editing?.data_fim_prevista ?? ""} />
            </Form.Group>
          </Col>
          <Col md={4}>
            <Form.Group>
              <Form.Label>Frequencia</Form.Label>
              <Form.Control name="frequencia" defaultValue={editing?.frequencia ?? ""} />
            </Form.Group>
          </Col>
          <Col md={12}>
            <Form.Group>
              <Form.Label>Descricao do Programa *</Form.Label>
              <Form.Control as="textarea" rows={4} name="programa_descricao" defaultValue={editing?.programa_descricao ?? ""} required />
            </Form.Group>
          </Col>
        </Row>
      </FormModal>
    </>
  );
}
