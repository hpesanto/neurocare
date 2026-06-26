import { useState } from "react";
import { Col, Form, Row } from "react-bootstrap";
import DataTable from "../../components/DataTable";
import FormModal from "../../components/FormModal";
import FkSelect from "../../components/FkSelect";
import TimeSelect from "../../components/TimeSelect";
import { useCrud } from "../../hooks/useCrud";
import { ENDPOINTS } from "../../api/endpoints";

interface Sessao {
  id: string;
  id_reabilitacao: string;
  data_sessao: string;
  hora_sessao: string | null;
  passos_realizados: string;
  proximos_passos_planejamento: string | null;
}

export default function SessoesReabPage() {
  const { items, isLoading, create, update, remove } = useCrud<Sessao>(ENDPOINTS.reabilitacaoSessao);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<Sessao | null>(null);

  const handleSubmit = async (data: Record<string, string>) => {
    const cleaned: Record<string, string | null> = {};
    for (const [k, v] of Object.entries(data)) {
      cleaned[k] = v === "" ? null : v;
    }
    if (editing) {
      await update({ id: editing.id, ...cleaned } as unknown as Sessao);
    } else {
      await create(cleaned as unknown as Sessao);
    }
  };

  return (
    <>
      <DataTable
        title="Sessoes de Reabilitacao"
        columns={[
          { key: "data_sessao", label: "Data" },
          { key: "hora_sessao", label: "Hora" },
          { key: "passos_realizados", label: "Passos Realizados" },
        ]}
        items={items}
        isLoading={isLoading}
        onAdd={() => { setEditing(null); setModalOpen(true); }}
        onEdit={(item) => { setEditing(item); setModalOpen(true); }}
        onDelete={(id) => { if (confirm("Excluir sessao?")) remove(id); }}
      />
      <FormModal
        title={editing ? "Editar Sessao" : "Nova Sessao de Reabilitacao"}
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        onSubmit={handleSubmit}
      >
        <Row className="g-3">
          <Col md={12}>
            <FkSelect name="id_reabilitacao" label="Reabilitacao" endpoint={ENDPOINTS.reabilitacaoNeuropsicologica} labelField="programa_descricao" defaultValue={editing?.id_reabilitacao} required />
          </Col>
          <Col md={6}>
            <Form.Group>
              <Form.Label>Data *</Form.Label>
              <Form.Control name="data_sessao" type="date" defaultValue={editing?.data_sessao ?? ""} required />
            </Form.Group>
          </Col>
          <Col md={6}>
            <TimeSelect name="hora_sessao" label="Hora" defaultValue={editing?.hora_sessao} />
          </Col>
          <Col md={12}>
            <Form.Group>
              <Form.Label>Passos Realizados *</Form.Label>
              <Form.Control as="textarea" rows={4} name="passos_realizados" defaultValue={editing?.passos_realizados ?? ""} required />
            </Form.Group>
          </Col>
          <Col md={12}>
            <Form.Group>
              <Form.Label>Proximos Passos</Form.Label>
              <Form.Control as="textarea" rows={3} name="proximos_passos_planejamento" defaultValue={editing?.proximos_passos_planejamento ?? ""} />
            </Form.Group>
          </Col>
        </Row>
      </FormModal>
    </>
  );
}
