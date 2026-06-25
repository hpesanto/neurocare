import { useState } from "react";
import { Col, Form, Row } from "react-bootstrap";
import DataTable from "../../components/DataTable";
import FormModal from "../../components/FormModal";
import { useCrud } from "../../hooks/useCrud";
import { ENDPOINTS } from "../../api/endpoints";
import type { TransacaoFinanceira } from "../../types/models";

export default function TransacoesPage() {
  const { items, isLoading, create, update, remove } = useCrud<TransacaoFinanceira>(ENDPOINTS.transacoes);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<TransacaoFinanceira | null>(null);

  const handleSubmit = async (data: Record<string, string>) => {
    const cleaned: Record<string, string | null> = {};
    for (const [k, v] of Object.entries(data)) {
      cleaned[k] = v === "" ? null : v;
    }
    if (editing) {
      await update({ id: editing.id, ...cleaned } as unknown as TransacaoFinanceira);
    } else {
      await create(cleaned as unknown as TransacaoFinanceira);
    }
  };

  return (
    <>
      <DataTable
        title="Transacoes Financeiras"
        columns={[
          { key: "data_transacao", label: "Data" },
          { key: "paciente_nome", label: "Paciente" },
          { key: "tipo_transacao_nome", label: "Tipo" },
          { key: "valor", label: "Valor (R$)" },
          { key: "forma_pagamento_nome", label: "Pagamento" },
          { key: "status_pagamento_nome", label: "Status" },
        ]}
        items={items}
        isLoading={isLoading}
        onAdd={() => { setEditing(null); setModalOpen(true); }}
        onEdit={(item) => { setEditing(item); setModalOpen(true); }}
        onDelete={(id) => { if (confirm("Excluir transacao?")) remove(id); }}
      />
      <FormModal
        title={editing ? "Editar Transacao" : "Nova Transacao"}
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        onSubmit={handleSubmit}
      >
        <Row className="g-3">
          <Col md={4}>
            <Form.Group>
              <Form.Label>Data *</Form.Label>
              <Form.Control name="data_transacao" type="date" defaultValue={editing?.data_transacao ?? ""} required />
            </Form.Group>
          </Col>
          <Col md={4}>
            <Form.Group>
              <Form.Label>Valor *</Form.Label>
              <Form.Control name="valor" type="number" step="0.01" defaultValue={editing?.valor ?? ""} required />
            </Form.Group>
          </Col>
          <Col md={4}>
            <Form.Group>
              <Form.Label>ID Tipo Transacao *</Form.Label>
              <Form.Control name="id_tipo_transacao" defaultValue={editing?.id_tipo_transacao ?? ""} required />
            </Form.Group>
          </Col>
          <Col md={6}>
            <Form.Group>
              <Form.Label>ID Forma Pagamento *</Form.Label>
              <Form.Control name="id_forma_pagamento" defaultValue={editing?.id_forma_pagamento ?? ""} required />
            </Form.Group>
          </Col>
          <Col md={6}>
            <Form.Group>
              <Form.Label>ID Status Pagamento *</Form.Label>
              <Form.Control name="id_status_pagamento" defaultValue={editing?.id_status_pagamento ?? ""} required />
            </Form.Group>
          </Col>
          <Col md={12}>
            <Form.Group>
              <Form.Label>Descricao *</Form.Label>
              <Form.Control as="textarea" rows={3} name="descricao" defaultValue={editing?.descricao ?? ""} required />
            </Form.Group>
          </Col>
        </Row>
      </FormModal>
    </>
  );
}
