import { useState } from "react";
import { Button } from "react-bootstrap";
import DataTable from "../../components/DataTable";
import FilterBar, { type FilterField } from "../../components/FilterBar";
import api from "../../api/client";
import { useEffect } from "react";

interface AuditLog {
  id: number;
  data_hora: string;
  usuario_login: string;
  perfil: string;
  acao: string;
  entidade: string;
  objeto_id: string;
  objeto_repr: string;
  alteracoes: Record<string, any> | null;
  ip: string;
  user_agent: string;
  metodo_http: string;
  caminho: string;
}

const FILTER_FIELDS: FilterField[] = [
  { name: "data_hora__gte", label: "Data Inicial", type: "date" },
  { name: "data_hora__lte", label: "Data Final", type: "date" },
  { name: "acao", label: "Ação", type: "select", options: [
    { value: "LOGIN", label: "Login" },
    { value: "LOGIN_FALHA", label: "Login Falha" },
    { value: "LOGOUT", label: "Logout" },
    { value: "CREATE", label: "Criação" },
    { value: "UPDATE", label: "Alteração" },
    { value: "DELETE", label: "Exclusão" },
    { value: "LEITURA", label: "Leitura" },
  ] },
  { name: "entidade", label: "Entidade", type: "text" },
  { name: "search", label: "Usuário/Objeto", type: "text" },
];

export default function AuditoriaPage() {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [filters, setFilters] = useState<Record<string, string>>({});

  const fetchLogs = async () => {
    setIsLoading(true);
    try {
      const params = new URLSearchParams(filters);
      const { data } = await api.get(`/auditoria/?${params}`);
      setLogs(Array.isArray(data) ? data : data.results || []);
    } catch (error: any) {
      const message = error.response?.status === 403
        ? "Acesso negado. Você precisa ser administrador."
        : "Erro ao carregar logs";
      alert(message);
      console.error("Erro:", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, [filters]);

  const exportar = async (formato: string) => {
    try {
      const params = new URLSearchParams({ formato, ...filters });
      const resp = await api.get(`/auditoria/exportar/?${params}`, { responseType: "blob" });
      const ext = formato === "xlsx" ? "xlsx" : "csv";
      const url = URL.createObjectURL(resp.data as Blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `auditoria.${ext}`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (error) {
      alert("Erro ao exportar");
      console.error("Erro:", error);
    }
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleString("pt-BR");
  };

  const getAcaoColor = (acao: string) => {
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
  };

  return (
    <>
      <FilterBar fields={FILTER_FIELDS} onApply={setFilters} onClear={() => setFilters({})} />
      <DataTable
        title="Log de Auditoria"
        columns={[
          { key: "data_hora", label: "Data/Hora", render: (v) => formatDate(v) },
          { key: "acao", label: "Ação", render: (v) => (
            <span className={`badge bg-${getAcaoColor(v)}`}>{v}</span>
          ) },
          { key: "usuario_login", label: "Usuário" },
          { key: "entidade", label: "Entidade" },
          { key: "objeto_repr", label: "Objeto" },
          { key: "ip", label: "IP" },
        ]}
        items={logs}
        isLoading={isLoading}
        onAdd={() => {}}
        onEdit={() => alert("Log é imutável - somente leitura")}
        onDelete={() => alert("Log é imutável - somente leitura")}
      />
      <div className="d-flex gap-2 mt-3">
        <Button variant="outline-success" size="sm" onClick={() => exportar("csv")}>
          <i className="bi bi-filetype-csv me-1" /> Exportar CSV
        </Button>
        <Button variant="outline-success" size="sm" onClick={() => exportar("xlsx")}>
          <i className="bi bi-file-earmark-excel me-1" /> Exportar Excel
        </Button>
      </div>
    </>
  );
}
