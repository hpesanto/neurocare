import { useState } from "react";
import { Col, Form, Row } from "react-bootstrap";
import DataTable from "../../components/DataTable";
import FormModal from "../../components/FormModal";
import { useCrud } from "../../hooks/useCrud";
import { ENDPOINTS } from "../../api/endpoints";

interface Produto {
  id: string;
  nome: string;
  descricao: string | null;
  valor_unitario: string;
  ativo: boolean;
  tipo_produto_nome: string | null;
  id_tipo_produto: string | null;
}

export default function ProdutosPage() {
  const { items, isLoading, create, update, remove } = useCrud<Produto>(ENDPOINTS.produtos);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<Produto | null>(null);

  const handleSubmit = async (data: Record<string, string>) => {
    const cleaned: Record<string, string | null> = {};
    for (const [k, v] of Object.entries(data)) {
      cleaned[k] = v === "" ? null : v;
    }
    if (editing) {
      await update({ id: editing.id, ...cleaned } as unknown as Produto);
    } else {
      await create(cleaned as unknown as Produto);
    }
  };

  return (
    <>
      <DataTable
        title="Produtos"
        columns={[
          { key: "nome", label: "Nome" },
          { key: "tipo_produto_nome", label: "Tipo" },
          { key: "valor_unitario", label: "Valor (R$)" },
          { key: "ativo", label: "Ativo", render: (i) => (i.ativo ? "Sim" : "Nao") },
        ]}
        items={items}
        isLoading={isLoading}
        onAdd={() => { setEditing(null); setModalOpen(true); }}
        onEdit={(item) => { setEditing(item); setModalOpen(true); }}
        onDelete={(id) => { if (confirm("Excluir produto?")) remove(id); }}
      />
      <FormModal
        title={editing ? `Editar ${editing.nome}` : "Novo Produto"}
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        onSubmit={handleSubmit}
      >
        <Row className="g-3">
          <Col md={8}>
            <Form.Group>
              <Form.Label>Nome *</Form.Label>
              <Form.Control name="nome" defaultValue={editing?.nome ?? ""} required />
            </Form.Group>
          </Col>
          <Col md={4}>
            <Form.Group>
              <Form.Label>Valor Unitario *</Form.Label>
              <Form.Control name="valor_unitario" type="number" step="0.01" defaultValue={editing?.valor_unitario ?? ""} required />
            </Form.Group>
          </Col>
          <Col md={12}>
            <Form.Group>
              <Form.Label>Descricao</Form.Label>
              <Form.Control as="textarea" rows={2} name="descricao" defaultValue={editing?.descricao ?? ""} />
            </Form.Group>
          </Col>
        </Row>
      </FormModal>
    </>
  );
}
