import { useState } from "react";
import { Button, Col, Form, Row } from "react-bootstrap";
import DataTable from "../../components/DataTable";
import FormModal from "../../components/FormModal";
import FkSelect from "../../components/FkSelect";
import FilterBar, { type FilterField } from "../../components/FilterBar";
import api from "../../api/client";
import { useCrud } from "../../hooks/useCrud";
import { ENDPOINTS } from "../../api/endpoints";
import type { TransacaoFinanceira } from "../../types/models";

const FILTER_FIELDS: FilterField[] = [
  { name: "data_transacao__gte", label: "Data inicio", type: "date" },
  { name: "data_transacao__lte", label: "Data fim", type: "date" },
  { name: "id_tipo_transacao", label: "Tipo", type: "fk-select", endpoint: ENDPOINTS.tiposTransacao },
  { name: "id_status_pagamento", label: "Status", type: "fk-select", endpoint: ENDPOINTS.statusPagamento },
];

export default function TransacoesPage() {
  const [filters, setFilters] = useState<Record<string, string>>({});
  const { items, isLoading, create, update, remove } = useCrud<TransacaoFinanceira>(ENDPOINTS.transacoes, filters);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<TransacaoFinanceira | null>(null);

  const exportar = async (formato: string) => {
    const params = new URLSearchParams({ formato, ...filters });
    const resp = await api.get(`/transacoes/exportar/?${params}`, { responseType: "blob" });
    const ext = formato === "xlsx" ? "xlsx" : "csv";
    const url = URL.createObjectURL(resp.data as Blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `transacoes.${ext}`;
    a.click();
    URL.revokeObjectURL(url);
  };

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
      <FilterBar fields={FILTER_FIELDS} onApply={setFilters} onClear={() => setFilters({})} />
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
      <div className="d-flex gap-2 mt-3">
        <Button variant="outline-success" size="sm" onClick={() => exportar("csv")}>
          <i className="bi bi-filetype-csv me-1" /> Exportar CSV
        </Button>
        <Button variant="outline-success" size="sm" onClick={() => exportar("xlsx")}>
          <i className="bi bi-file-earmark-excel me-1" /> Exportar Excel
        </Button>
      </div>
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
            <FkSelect name="id_tipo_transacao" label="Tipo de Transacao" endpoint={ENDPOINTS.tiposTransacao} defaultValue={editing?.id_tipo_transacao} required />
          </Col>
          <Col md={4}>
            <FkSelect name="id_forma_pagamento" label="Forma de Pagamento" endpoint={ENDPOINTS.formasPagamento} defaultValue={editing?.id_forma_pagamento} required />
          </Col>
          <Col md={4}>
            <FkSelect name="id_status_pagamento" label="Status Pagamento" endpoint={ENDPOINTS.statusPagamento} defaultValue={editing?.id_status_pagamento} required />
          </Col>
          <Col md={4}>
            <FkSelect name="id_paciente" label="Paciente" endpoint={ENDPOINTS.pacientes} labelField="nome_completo" defaultValue={editing?.id_paciente ?? undefined} />
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
