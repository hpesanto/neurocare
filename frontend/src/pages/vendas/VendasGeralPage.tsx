import { useState } from "react";
import { Col, Form, Row } from "react-bootstrap";
import DataTable from "../../components/DataTable";
import FormModal from "../../components/FormModal";
import { useCrud } from "../../hooks/useCrud";
import { ENDPOINTS } from "../../api/endpoints";

interface VendaGeral {
  id: string;
  data_venda: string;
  nome_comprador: string | null;
  contato_comprador: string | null;
  valor_total_transacao: string;
  id_forma_pagamento: string;
}

export default function VendasGeralPage() {
  const { items, isLoading, create, update, remove } = useCrud<VendaGeral>(ENDPOINTS.vendasGeral);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<VendaGeral | null>(null);

  const handleSubmit = async (data: Record<string, string>) => {
    const cleaned: Record<string, string | null> = {};
    for (const [k, v] of Object.entries(data)) {
      cleaned[k] = v === "" ? null : v;
    }
    if (editing) {
      await update({ id: editing.id, ...cleaned } as unknown as VendaGeral);
    } else {
      await create(cleaned as unknown as VendaGeral);
    }
  };

  return (
    <>
      <DataTable
        title="Vendas Gerais"
        columns={[
          { key: "data_venda", label: "Data" },
          { key: "nome_comprador", label: "Comprador" },
          { key: "contato_comprador", label: "Contato" },
          { key: "valor_total_transacao", label: "Total (R$)" },
        ]}
        items={items}
        isLoading={isLoading}
        onAdd={() => { setEditing(null); setModalOpen(true); }}
        onEdit={(item) => { setEditing(item); setModalOpen(true); }}
        onDelete={(id) => { if (confirm("Excluir venda?")) remove(id); }}
      />
      <FormModal
        title={editing ? "Editar Venda" : "Nova Venda Geral"}
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        onSubmit={handleSubmit}
      >
        <Row className="g-3">
          <Col md={4}>
            <Form.Group>
              <Form.Label>Data *</Form.Label>
              <Form.Control name="data_venda" type="date" defaultValue={editing?.data_venda ?? ""} required />
            </Form.Group>
          </Col>
          <Col md={4}>
            <Form.Group>
              <Form.Label>Valor Total *</Form.Label>
              <Form.Control name="valor_total_transacao" type="number" step="0.01" defaultValue={editing?.valor_total_transacao ?? ""} required />
            </Form.Group>
          </Col>
          <Col md={4}>
            <Form.Group>
              <Form.Label>ID Forma Pagamento *</Form.Label>
              <Form.Control name="id_forma_pagamento" defaultValue={editing?.id_forma_pagamento ?? ""} required />
            </Form.Group>
          </Col>
          <Col md={6}>
            <Form.Group>
              <Form.Label>Comprador</Form.Label>
              <Form.Control name="nome_comprador" defaultValue={editing?.nome_comprador ?? ""} />
            </Form.Group>
          </Col>
          <Col md={6}>
            <Form.Group>
              <Form.Label>Contato</Form.Label>
              <Form.Control name="contato_comprador" defaultValue={editing?.contato_comprador ?? ""} />
            </Form.Group>
          </Col>
        </Row>
      </FormModal>
    </>
  );
}
