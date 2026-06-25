import { useState } from "react";
import { Col, Form, Row } from "react-bootstrap";
import DataTable from "../../components/DataTable";
import FormModal from "../../components/FormModal";
import FkSelect from "../../components/FkSelect";
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
        <Row className="g-3">
          <Col md={6}>
            <FkSelect name="id_paciente" label="Paciente" endpoint={ENDPOINTS.pacientes} labelField="nome_completo" defaultValue={editing?.id_paciente} required />
          </Col>
          <Col md={6}>
            <Form.Group>
              <Form.Label>Nome do Contato *</Form.Label>
              <Form.Control name="nome_contato" defaultValue={editing?.nome_contato ?? ""} required />
            </Form.Group>
          </Col>
          <Col md={6}>
            <Form.Group>
              <Form.Label>Telefone *</Form.Label>
              <Form.Control name="telefone_contato" defaultValue={editing?.telefone_contato ?? ""} required />
            </Form.Group>
          </Col>
          <Col md={6}>
            <Form.Group>
              <Form.Label>Parentesco *</Form.Label>
              <Form.Control name="parentesco" defaultValue={editing?.parentesco ?? ""} required />
            </Form.Group>
          </Col>
        </Row>
      </FormModal>
    </>
  );
}
