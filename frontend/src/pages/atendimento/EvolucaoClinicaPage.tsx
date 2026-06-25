import { useState } from "react";
import { Col, Form, Row } from "react-bootstrap";
import DataTable from "../../components/DataTable";
import FormModal from "../../components/FormModal";
import FkSelect from "../../components/FkSelect";
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
        <Row className="g-3">
          <Col md={6}>
            <FkSelect name="id_paciente" label="Paciente" endpoint={ENDPOINTS.pacientes} labelField="nome_completo" defaultValue={editing?.id_paciente} required />
          </Col>
          <Col md={6}>
            <FkSelect name="id_psicologo" label="Psicologo" endpoint={ENDPOINTS.profissionais} labelField="nome" defaultValue={editing?.id_psicologo} required />
          </Col>
          <Col md={6}>
            <Form.Group>
              <Form.Label>Data *</Form.Label>
              <Form.Control name="data_sessao" type="date" defaultValue={editing?.data_sessao ?? ""} required />
            </Form.Group>
          </Col>
          <Col md={6}>
            <Form.Group>
              <Form.Label>Hora</Form.Label>
              <Form.Control name="hora_sessao" type="time" defaultValue={editing?.hora_sessao ?? ""} />
            </Form.Group>
          </Col>
          <Col md={12}>
            <Form.Group>
              <Form.Label>Evolucao *</Form.Label>
              <Form.Control as="textarea" rows={5} name="evolucao_texto" defaultValue={editing?.evolucao_texto ?? ""} required />
            </Form.Group>
          </Col>
        </Row>
      </FormModal>
    </>
  );
}
