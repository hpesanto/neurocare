import { useState } from "react";
import { Col, Form, Row } from "react-bootstrap";
import DataTable from "../../components/DataTable";
import FormModal from "../../components/FormModal";
import FkSelect from "../../components/FkSelect";
import { useCrud } from "../../hooks/useCrud";
import { ENDPOINTS } from "../../api/endpoints";

interface Objetivo {
  id: string;
  id_reabilitacao: string;
  paciente_nome: string | null;
  profissional_nome: string | null;
  descricao: string;
  id_status_objetivo: string | null;
  status_nome: string | null;
  comentario_status: string | null;
}

export default function ObjetivosReabPage() {
  const { items, isLoading, create, update, remove } = useCrud<Objetivo>(ENDPOINTS.reabilitacaoObjetivo);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<Objetivo | null>(null);

  const handleSubmit = async (data: Record<string, string>) => {
    const cleaned: Record<string, string | null> = {};
    for (const [k, v] of Object.entries(data)) {
      cleaned[k] = v === "" ? null : v;
    }
    if (editing) {
      await update({ id: editing.id, ...cleaned } as unknown as Objetivo);
    } else {
      await create(cleaned as unknown as Objetivo);
    }
  };

  return (
    <>
      <DataTable
        title="Objetivos de Reabilitacao"
        columns={[
          { key: "paciente_nome", label: "Paciente" },
          { key: "profissional_nome", label: "Profissional" },
          { key: "descricao", label: "Descricao" },
          { key: "status_nome", label: "Status" },
          { key: "comentario_status", label: "Comentario" },
        ]}
        items={items}
        isLoading={isLoading}
        onAdd={() => { setEditing(null); setModalOpen(true); }}
        onEdit={(item) => { setEditing(item); setModalOpen(true); }}
        onDelete={(id) => { if (confirm("Excluir objetivo?")) remove(id); }}
      />
      <FormModal
        title={editing ? "Editar Objetivo" : "Novo Objetivo de Reabilitacao"}
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        onSubmit={handleSubmit}
      >
        <Row className="g-3">
          <Col md={6}>
            <FkSelect name="id_reabilitacao" label="Reabilitacao" endpoint={ENDPOINTS.reabilitacaoNeuropsicologica} labelField="programa_descricao" defaultValue={editing?.id_reabilitacao} required />
          </Col>
          <Col md={6}>
            <FkSelect name="id_status_objetivo" label="Status" endpoint={ENDPOINTS.statusObjetivoReabilitacao} defaultValue={editing?.id_status_objetivo ?? undefined} />
          </Col>
          <Col md={12}>
            <Form.Group>
              <Form.Label>Descricao *</Form.Label>
              <Form.Control as="textarea" rows={3} name="descricao" defaultValue={editing?.descricao ?? ""} required />
            </Form.Group>
          </Col>
          <Col md={12}>
            <Form.Group>
              <Form.Label>Comentario</Form.Label>
              <Form.Control as="textarea" rows={2} name="comentario_status" defaultValue={editing?.comentario_status ?? ""} />
            </Form.Group>
          </Col>
        </Row>
      </FormModal>
    </>
  );
}
