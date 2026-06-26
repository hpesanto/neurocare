import { useEffect, useState } from "react";
import { Badge, Button, Card, Col, Row, Spinner, Tab, Table, Tabs } from "react-bootstrap";
import { useNavigate, useParams } from "react-router-dom";
import api from "../../api/client";
import { ENDPOINTS } from "../../api/endpoints";
import type { Paciente } from "../../types/models";

interface RelatedItem {
  id: string;
  [key: string]: unknown;
}

function RelatedTable({ endpoint, filters, columns }: {
  endpoint: string;
  filters: Record<string, string>;
  columns: { key: string; label: string }[];
}) {
  const [items, setItems] = useState<RelatedItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const params = new URLSearchParams(filters);
    api.get(`${endpoint}?${params}&page_size=100`).then((r) => {
      setItems(r.data.results ?? []);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, [endpoint, filters]);

  if (loading) return <Spinner animation="border" size="sm" />;
  if (items.length === 0) return <p className="text-muted py-3 text-center">Nenhum registro</p>;

  return (
    <Table hover size="sm" className="mb-0">
      <thead className="table-light">
        <tr>
          {columns.map((c) => <th key={c.key}>{c.label}</th>)}
        </tr>
      </thead>
      <tbody>
        {items.map((item) => (
          <tr key={item.id}>
            {columns.map((c) => (
              <td key={c.key}>{String(item[c.key] ?? "—")}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </Table>
  );
}

function InfoRow({ label, value }: { label: string; value: string | null | undefined }) {
  return (
    <Col md={4} className="mb-2">
      <small className="text-muted d-block">{label}</small>
      <span>{value || "—"}</span>
    </Col>
  );
}

export default function PacienteDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [paciente, setPaciente] = useState<Paciente | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    api.get(`${ENDPOINTS.pacientes}${id}/`).then((r) => {
      setPaciente(r.data);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="text-center py-5"><Spinner animation="border" /></div>;
  if (!paciente) return <p>Paciente nao encontrado</p>;

  const filters = { id_paciente: paciente.id };

  return (
    <>
      <div className="d-flex align-items-center gap-3 mb-4">
        <Button variant="outline-secondary" size="sm" onClick={() => navigate("/cadastro/pacientes")}>
          <i className="bi bi-arrow-left me-1" /> Voltar
        </Button>
        <h4 className="mb-0">{paciente.nome_completo}</h4>
        {paciente.status_paciente && (
          <Badge bg={paciente.status_paciente === "Ativo" ? "success" : "secondary"}>
            {paciente.status_paciente}
          </Badge>
        )}
      </div>

      <Tabs defaultActiveKey="dados" className="mb-3">
        <Tab eventKey="dados" title={<><i className="bi bi-person me-1" />Dados</>}>
          <Card>
            <Card.Body>
              <h6 className="text-muted text-uppercase small fw-bold mb-3">Dados pessoais</h6>
              <Row>
                <InfoRow label="Nome Completo" value={paciente.nome_completo} />
                <InfoRow label="Data Nascimento" value={paciente.data_nascimento} />
                <InfoRow label="CPF" value={paciente.cpf} />
                <InfoRow label="RG" value={paciente.rg} />
                <InfoRow label="Genero" value={paciente.genero} />
                <InfoRow label="Estado Civil" value={paciente.estado_civil} />
                <InfoRow label="Profissao" value={paciente.profissao} />
              </Row>
              <h6 className="text-muted text-uppercase small fw-bold mt-3 mb-3">Contato</h6>
              <Row>
                <InfoRow label="Telefone" value={paciente.telefone_principal} />
                <InfoRow label="Telefone 2" value={paciente.telefone_secundario} />
                <InfoRow label="Email" value={paciente.email} />
              </Row>
              <h6 className="text-muted text-uppercase small fw-bold mt-3 mb-3">Endereco</h6>
              <Row>
                <InfoRow label="Rua" value={paciente.endereco_rua} />
                <InfoRow label="Numero" value={paciente.endereco_numero} />
                <InfoRow label="Complemento" value={paciente.endereco_complemento} />
                <InfoRow label="Bairro" value={paciente.endereco_bairro} />
                <InfoRow label="Cidade" value={paciente.endereco_cidade} />
                <InfoRow label="Estado" value={paciente.endereco_estado} />
                <InfoRow label="CEP" value={paciente.endereco_cep} />
              </Row>
              <h6 className="text-muted text-uppercase small fw-bold mt-3 mb-3">Convenio e encaminhamento</h6>
              <Row>
                <InfoRow label="Psicologo Responsavel" value={paciente.psicologo_nome} />
                <InfoRow label="Convenio" value={paciente.convenio_nome} />
                <InfoRow label="Faixa Etaria" value={paciente.faixa_etaria_nome} />
                <InfoRow label="Quem Encaminhou" value={paciente.quem_encaminhou} />
                <InfoRow label="Carteirinha" value={paciente.numero_carteirinha_convenio} />
                <InfoRow label="Validade" value={paciente.validade_carteirinha_convenio} />
              </Row>
              {paciente.observacoes_gerais && (
                <>
                  <h6 className="text-muted text-uppercase small fw-bold mt-3 mb-2">Observacoes</h6>
                  <p>{paciente.observacoes_gerais}</p>
                </>
              )}
            </Card.Body>
          </Card>
        </Tab>

        <Tab eventKey="evolucao" title={<><i className="bi bi-journal-medical me-1" />Evolucao</>}>
          <Card>
            <Card.Body className="p-0">
              <RelatedTable
                endpoint={ENDPOINTS.evolucaoClinica}
                filters={filters}
                columns={[
                  { key: "data_sessao", label: "Data" },
                  { key: "hora_sessao", label: "Hora" },
                  { key: "psicologo_nome", label: "Psicologo" },
                  { key: "evolucao_texto", label: "Evolucao" },
                ]}
              />
            </Card.Body>
          </Card>
        </Tab>

        <Tab eventKey="avaliacao" title={<><i className="bi bi-clipboard2-pulse me-1" />Avaliacao</>}>
          <Card>
            <Card.Body className="p-0">
              <RelatedTable
                endpoint={ENDPOINTS.avaliacaoNeuropsicologica}
                filters={filters}
                columns={[
                  { key: "data_avaliacao", label: "Data" },
                  { key: "psicologo_nome", label: "Psicologo" },
                  { key: "motivo_avaliacao", label: "Motivo" },
                  { key: "valor_avaliacao", label: "Valor" },
                ]}
              />
            </Card.Body>
          </Card>
        </Tab>

        <Tab eventKey="reabilitacao" title={<><i className="bi bi-heart-pulse me-1" />Reabilitacao</>}>
          <Card>
            <Card.Body className="p-0">
              <RelatedTable
                endpoint={ENDPOINTS.reabilitacaoNeuropsicologica}
                filters={filters}
                columns={[
                  { key: "data_inicio", label: "Inicio" },
                  { key: "data_fim_prevista", label: "Fim Previsto" },
                  { key: "psicologo_nome", label: "Psicologo" },
                  { key: "programa_descricao", label: "Programa" },
                ]}
              />
            </Card.Body>
          </Card>
        </Tab>

        <Tab eventKey="vendas" title={<><i className="bi bi-cart me-1" />Vendas</>}>
          <Card>
            <Card.Body className="p-0">
              <RelatedTable
                endpoint={ENDPOINTS.vendasVinculadas}
                filters={filters}
                columns={[
                  { key: "data_venda", label: "Data" },
                  { key: "produto_nome", label: "Produto" },
                  { key: "quantidade", label: "Qtd" },
                  { key: "valor_total_produto", label: "Total" },
                ]}
              />
            </Card.Body>
          </Card>
        </Tab>
      </Tabs>
    </>
  );
}
