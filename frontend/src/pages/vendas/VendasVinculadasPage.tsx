import { useState } from "react";
import { Col, Form, Row } from "react-bootstrap";
import DataTable from "../../components/DataTable";
import FormModal from "../../components/FormModal";
import { useCrud } from "../../hooks/useCrud";
import { ENDPOINTS } from "../../api/endpoints";

interface VendaVinculada {
  id: string;
  id_paciente: string;
  paciente_nome: string | null;
  id_produto: string;
  produto_nome: string | null;
  id_forma_pagamento: string;
  data_venda: string;
  quantidade: number;
  valor_unitario: string;
  valor_total_produto: string;
}

export default function VendasVinculadasPage() {
  const { items, isLoading, create, update, remove } = useCrud<VendaVinculada>(ENDPOINTS.vendasVinculadas);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<VendaVinculada | null>(null);

  const handleSubmit = async (data: Record<string, string>) => {
    const cleaned: Record<string, string | null> = {};
    for (const [k, v] of Object.entries(data)) {
      cleaned[k] = v === "" ? null : v;
    }
    if (editing) {
      await update({ id: editing.id, ...cleaned } as unknown as VendaVinculada);
    } else {
      await create(cleaned as unknown as VendaVinculada);
    }
  };

  return (
    <>
      <DataTable
        title="Vendas Vinculadas ao Paciente"
        columns={[
          { key: "data_venda", label: "Data" },
          { key: "paciente_nome", label: "Paciente" },
          { key: "produto_nome", label: "Produto" },
          { key: "quantidade", label: "Qtd" },
          { key: "valor_unitario", label: "Valor Unit." },
          { key: "valor_total_produto", label: "Total" },
        ]}
        items={items}
        isLoading={isLoading}
        onAdd={() => { setEditing(null); setModalOpen(true); }}
        onEdit={(item) => { setEditing(item); setModalOpen(true); }}
        onDelete={(id) => { if (confirm("Excluir venda?")) remove(id); }}
      />
      <FormModal
        title={editing ? "Editar Venda" : "Nova Venda Vinculada"}
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
              <Form.Label>Quantidade *</Form.Label>
              <Form.Control name="quantidade" type="number" defaultValue={editing?.quantidade ?? ""} required />
            </Form.Group>
          </Col>
          <Col md={4}>
            <Form.Group>
              <Form.Label>Valor Unitario *</Form.Label>
              <Form.Control name="valor_unitario" type="number" step="0.01" defaultValue={editing?.valor_unitario ?? ""} required />
            </Form.Group>
          </Col>
          <Col md={4}>
            <Form.Group>
              <Form.Label>Valor Total *</Form.Label>
              <Form.Control name="valor_total_produto" type="number" step="0.01" defaultValue={editing?.valor_total_produto ?? ""} required />
            </Form.Group>
          </Col>
          <Col md={4}>
            <Form.Group>
              <Form.Label>ID Paciente *</Form.Label>
              <Form.Control name="id_paciente" defaultValue={editing?.id_paciente ?? ""} required />
            </Form.Group>
          </Col>
          <Col md={4}>
            <Form.Group>
              <Form.Label>ID Produto *</Form.Label>
              <Form.Control name="id_produto" defaultValue={editing?.id_produto ?? ""} required />
            </Form.Group>
          </Col>
          <Col md={6}>
            <Form.Group>
              <Form.Label>ID Forma Pagamento *</Form.Label>
              <Form.Control name="id_forma_pagamento" defaultValue={editing?.id_forma_pagamento ?? ""} required />
            </Form.Group>
          </Col>
        </Row>
      </FormModal>
    </>
  );
}
