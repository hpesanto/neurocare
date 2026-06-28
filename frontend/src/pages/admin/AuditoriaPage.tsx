import { useState, useEffect } from "react";
import { Container, Row, Col, Button, Form, Table, Spinner, Alert } from "react-bootstrap";
import api from "../../api/client";

interface AuditLog {
  id: number;
  data_hora: string;
  usuario_login: string;
  perfil?: string;
  acao: string;
  entidade?: string;
  objeto_id?: string;
  objeto_repr?: string;
  ip?: string;
}

export default function AuditoriaPage() {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [filters, setFilters] = useState({
    acao: "",
    entidade: "",
    usuario: "",
  });

  const fetchLogs = async () => {
    setLoading(true);
    setError("");
    try {
      const params = new URLSearchParams();
      if (filters.acao) params.append("acao", filters.acao);
      if (filters.entidade) params.append("entidade", filters.entidade);
      if (filters.usuario) params.append("search", filters.usuario);

      const response = await api.get(`/auditoria/?${params}`);
      const data = Array.isArray(response.data) ? response.data : response.data.results || [];
      setLogs(data);
    } catch (err: any) {
      const msg = err.response?.status === 403
        ? "Acesso negado - você precisa ser admin"
        : err.message || "Erro ao carregar logs";
      setError(msg);
      console.error("Erro:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, []);

  const handleFilterChange = (e: any) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchLogs();
  };

  const handleExport = async (formato: string) => {
    try {
      const params = new URLSearchParams();
      params.append("formato", formato);
      if (filters.acao) params.append("acao", filters.acao);
      if (filters.entidade) params.append("entidade", filters.entidade);
      if (filters.usuario) params.append("search", filters.usuario);

      const response = await api.get(`/auditoria/exportar/?${params}`, {
        responseType: "blob",
      });

      const url = URL.createObjectURL(response.data as Blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `auditoria.${formato}`;
      link.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      alert("Erro ao exportar");
      console.error("Erro:", err);
    }
  };

  return (
    <Container className="mt-4">
      <h2>Log de Auditoria</h2>

      {/* Filtros */}
      <Form onSubmit={handleSearch} className="mb-4 p-3 bg-light rounded">
        <Row>
          <Col md={3}>
            <Form.Group>
              <Form.Label>Ação</Form.Label>
              <Form.Select name="acao" value={filters.acao} onChange={handleFilterChange}>
                <option value="">Todas</option>
                <option value="LOGIN">Login</option>
                <option value="LOGIN_FALHA">Login Falha</option>
                <option value="LOGOUT">Logout</option>
                <option value="CREATE">Criação</option>
                <option value="UPDATE">Alteração</option>
                <option value="DELETE">Exclusão</option>
                <option value="LEITURA">Leitura</option>
              </Form.Select>
            </Form.Group>
          </Col>
          <Col md={3}>
            <Form.Group>
              <Form.Label>Entidade</Form.Label>
              <Form.Control
                type="text"
                name="entidade"
                value={filters.entidade}
                onChange={handleFilterChange}
                placeholder="ex: Paciente"
              />
            </Form.Group>
          </Col>
          <Col md={3}>
            <Form.Group>
              <Form.Label>Usuário</Form.Label>
              <Form.Control
                type="text"
                name="usuario"
                value={filters.usuario}
                onChange={handleFilterChange}
                placeholder="ex: admin"
              />
            </Form.Group>
          </Col>
          <Col md={3} className="d-flex align-items-end gap-2">
            <Button variant="primary" type="submit" className="w-100">
              Buscar
            </Button>
          </Col>
        </Row>
      </Form>

      {/* Erros */}
      {error && <Alert variant="danger">{error}</Alert>}

      {/* Loading */}
      {loading && (
        <div className="text-center p-5">
          <Spinner animation="border" />
          <p className="mt-2">Carregando...</p>
        </div>
      )}

      {/* Tabela */}
      {!loading && logs.length === 0 && !error && (
        <Alert variant="info">Nenhum log encontrado</Alert>
      )}

      {!loading && logs.length > 0 && (
        <>
          <div className="table-responsive">
            <Table striped bordered hover>
              <thead>
                <tr>
                  <th>Data/Hora</th>
                  <th>Ação</th>
                  <th>Usuário</th>
                  <th>Entidade</th>
                  <th>Objeto</th>
                  <th>IP</th>
                </tr>
              </thead>
              <tbody>
                {logs.map((log) => (
                  <tr key={log.id}>
                    <td>{new Date(log.data_hora).toLocaleString("pt-BR")}</td>
                    <td>
                      <span className={`badge bg-${getAcaoBadgeColor(log.acao)}`}>
                        {log.acao}
                      </span>
                    </td>
                    <td>{log.usuario_login}</td>
                    <td>{log.entidade || "-"}</td>
                    <td>{log.objeto_repr || "-"}</td>
                    <td>{log.ip || "-"}</td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </div>

          {/* Export */}
          <div className="d-flex gap-2 mt-3">
            <Button variant="success" size="sm" onClick={() => handleExport("csv")}>
              <i className="bi bi-filetype-csv me-1" /> CSV
            </Button>
            <Button variant="success" size="sm" onClick={() => handleExport("xlsx")}>
              <i className="bi bi-file-earmark-excel me-1" /> Excel
            </Button>
          </div>
        </>
      )}
    </Container>
  );
}

function getAcaoBadgeColor(acao: string): string {
  const colors: Record<string, string> = {
    LOGIN: "success",
    LOGIN_FALHA: "danger",
    LOGOUT: "warning",
    CREATE: "info",
    UPDATE: "primary",
    DELETE: "danger",
    LEITURA: "secondary",
  };
  return colors[acao] || "light";
}
