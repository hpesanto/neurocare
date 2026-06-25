import { useState } from "react";
import { Col, Form, Row } from "react-bootstrap";
import DataTable from "../../components/DataTable";
import FormModal from "../../components/FormModal";
import FkSelect from "../../components/FkSelect";
import { useCrud } from "../../hooks/useCrud";
import { ENDPOINTS } from "../../api/endpoints";

interface Avaliacao {
  id: string;
  id_paciente: string;
  paciente_nome: string | null;
  id_psicologo: string;
  psicologo_nome: string | null;
  data_avaliacao: string;
  motivo_avaliacao: string;
  instrumentos_utilizados: string | null;
  valor_avaliacao: string | null;
  hipoteses_diagnosticas: string | null;
  resultados_principais: string | null;
  conclusao_recomendacoes: string | null;
}

export default function AvaliacaoPage() {
  const { items, isLoading, create, update, remove } = useCrud<Avaliacao>(ENDPOINTS.avaliacaoNeuropsicologica);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<Avaliacao | null>(null);

  const handleSubmit = async (data: Record<string, string>) => {
    const cleaned: Record<string, string | null> = {};
    for (const [k, v] of Object.entries(data)) {
      cleaned[k] = v === "" ? null : v;
    }
    if (editing) {
      await update({ id: editing.id, ...cleaned } as unknown as Avaliacao);
    } else {
      await create(cleaned as unknown as Avaliacao);
    }
  };

  return (
    <>
      <DataTable
        title="Avaliacao Neuropsicologica"
        columns={[
          { key: "paciente_nome", label: "Paciente" },
          { key: "psicologo_nome", label: "Psicologo" },
          { key: "data_avaliacao", label: "Data" },
          { key: "valor_avaliacao", label: "Valor (R$)" },
        ]}
        items={items}
        isLoading={isLoading}
        onAdd={() => { setEditing(null); setModalOpen(true); }}
        onEdit={(item) => { setEditing(item); setModalOpen(true); }}
        onDelete={(id) => { if (confirm("Excluir avaliacao?")) remove(id); }}
      />
      <FormModal
        title={editing ? "Editar Avaliacao" : "Nova Avaliacao Neuropsicologica"}
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        onSubmit={handleSubmit}
        size="xl"
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
              <Form.Label>Data da Avaliacao *</Form.Label>
              <Form.Control name="data_avaliacao" type="date" defaultValue={editing?.data_avaliacao ?? ""} required />
            </Form.Group>
          </Col>
          <Col md={4}>
            <Form.Group>
              <Form.Label>Valor (R$)</Form.Label>
              <Form.Control name="valor_avaliacao" type="number" step="0.01" defaultValue={editing?.valor_avaliacao ?? ""} />
            </Form.Group>
          </Col>
          <Col md={12}>
            <Form.Group>
              <Form.Label>Motivo da Avaliacao *</Form.Label>
              <Form.Control as="textarea" rows={3} name="motivo_avaliacao" defaultValue={editing?.motivo_avaliacao ?? ""} required />
            </Form.Group>
          </Col>
          <Col md={12}>
            <Form.Group>
              <Form.Label>Instrumentos Utilizados</Form.Label>
              <Form.Control as="textarea" rows={2} name="instrumentos_utilizados" defaultValue={editing?.instrumentos_utilizados ?? ""} />
            </Form.Group>
          </Col>
          <Col md={6}>
            <Form.Group>
              <Form.Label>Hipoteses Diagnosticas</Form.Label>
              <Form.Control as="textarea" rows={2} name="hipoteses_diagnosticas" defaultValue={editing?.hipoteses_diagnosticas ?? ""} />
            </Form.Group>
          </Col>
          <Col md={6}>
            <Form.Group>
              <Form.Label>Resultados Principais</Form.Label>
              <Form.Control as="textarea" rows={2} name="resultados_principais" defaultValue={editing?.resultados_principais ?? ""} />
            </Form.Group>
          </Col>
          <Col md={12}>
            <Form.Group>
              <Form.Label>Conclusao e Recomendacoes</Form.Label>
              <Form.Control as="textarea" rows={2} name="conclusao_recomendacoes" defaultValue={editing?.conclusao_recomendacoes ?? ""} />
            </Form.Group>
          </Col>
        </Row>
      </FormModal>
    </>
  );
}
