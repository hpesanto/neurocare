import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { api } from '../../services/api';

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

const ACAO_COLORS: Record<string, string> = {
  LOGIN: 'bg-green-100 text-green-800',
  LOGIN_FALHA: 'bg-red-100 text-red-800',
  LOGOUT: 'bg-yellow-100 text-yellow-800',
  CREATE: 'bg-blue-100 text-blue-800',
  UPDATE: 'bg-indigo-100 text-indigo-800',
  DELETE: 'bg-pink-100 text-pink-800',
  LEITURA: 'bg-gray-100 text-gray-800',
};

const AuditoriaPage: React.FC = () => {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [selectedLog, setSelectedLog] = useState<AuditLog | null>(null);
  const [loading, setLoading] = useState(false);
  const [searchParams, setSearchParams] = useSearchParams();

  const [filters, setFilters] = useState({
    acao: searchParams.get('acao') || '',
    entidade: searchParams.get('entidade') || '',
    usuario_login: searchParams.get('usuario_login') || '',
    data_inicio: searchParams.get('data_inicio') || '',
    data_fim: searchParams.get('data_fim') || '',
  });

  const fetchLogs = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (filters.acao) params.append('acao', filters.acao);
      if (filters.entidade) params.append('entidade', filters.entidade);
      if (filters.usuario_login) params.append('search', filters.usuario_login);
      if (filters.data_inicio) params.append('data_hora__gte', filters.data_inicio);
      if (filters.data_fim) params.append('data_hora__lte', filters.data_fim);

      const { data } = await api.get(`/auditoria/?${params}`);
      setLogs(data.results || data);
      setSearchParams(params);
    } catch (error) {
      console.error('Erro ao carregar logs:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, []);

  const handleFilterChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFilters(prev => ({ ...prev, [name]: value }));
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchLogs();
  };

  const handleExport = async (formato: 'csv' | 'xlsx') => {
    try {
      const params = new URLSearchParams();
      params.append('formato', formato);
      if (filters.acao) params.append('acao', filters.acao);
      if (filters.entidade) params.append('entidade', filters.entidade);
      if (filters.usuario_login) params.append('search', filters.usuario_login);
      if (filters.data_inicio) params.append('data_hora__gte', filters.data_inicio);
      if (filters.data_fim) params.append('data_hora__lte', filters.data_fim);

      const response = await api.get(`/auditoria/exportar/?${params}`, {
        responseType: 'blob',
      });

      const url = window.URL.createObjectURL(response.data);
      const a = document.createElement('a');
      a.href = url;
      a.download = `auditoria.${formato}`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error(`Erro ao exportar ${formato}:`, error);
    }
  };

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Log de Auditoria</h1>

      {/* Filtros */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <form onSubmit={handleSearch} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Ação</label>
              <select
                name="acao"
                value={filters.acao}
                onChange={handleFilterChange}
                className="w-full px-3 py-2 border rounded"
              >
                <option value="">Todas</option>
                <option value="LOGIN">Login</option>
                <option value="LOGIN_FALHA">Login Falha</option>
                <option value="LOGOUT">Logout</option>
                <option value="CREATE">Criação</option>
                <option value="UPDATE">Alteração</option>
                <option value="DELETE">Exclusão</option>
                <option value="LEITURA">Leitura</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Entidade</label>
              <input
                type="text"
                name="entidade"
                value={filters.entidade}
                onChange={handleFilterChange}
                placeholder="ex: Paciente"
                className="w-full px-3 py-2 border rounded"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Usuário</label>
              <input
                type="text"
                name="usuario_login"
                value={filters.usuario_login}
                onChange={handleFilterChange}
                placeholder="ex: psicologa1"
                className="w-full px-3 py-2 border rounded"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Data Inicial</label>
              <input
                type="date"
                name="data_inicio"
                value={filters.data_inicio}
                onChange={handleFilterChange}
                className="w-full px-3 py-2 border rounded"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Data Final</label>
              <input
                type="date"
                name="data_fim"
                value={filters.data_fim}
                onChange={handleFilterChange}
                className="w-full px-3 py-2 border rounded"
              />
            </div>
          </div>

          <div className="flex gap-2">
            <button
              type="submit"
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
              Buscar
            </button>
            <button
              type="button"
              onClick={() => handleExport('csv')}
              className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
            >
              📥 CSV
            </button>
            <button
              type="button"
              onClick={() => handleExport('xlsx')}
              className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
            >
              📥 XLSX
            </button>
          </div>
        </form>
      </div>

      {/* Lista de Logs */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {loading ? (
          <div className="p-6 text-center text-gray-500">Carregando...</div>
        ) : logs.length === 0 ? (
          <div className="p-6 text-center text-gray-500">Nenhum log encontrado</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b">
                <tr>
                  <th className="px-4 py-3 text-left text-sm font-semibold">Data/Hora</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold">Ação</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold">Usuário</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold">Entidade</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold">Objeto</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold">IP</th>
                </tr>
              </thead>
              <tbody>
                {logs.map((log) => (
                  <tr
                    key={log.id}
                    onClick={() => setSelectedLog(log)}
                    className="border-b hover:bg-gray-50 cursor-pointer"
                  >
                    <td className="px-4 py-3 text-sm text-gray-600">
                      {new Date(log.data_hora).toLocaleString('pt-BR')}
                    </td>
                    <td className="px-4 py-3 text-sm">
                      <span className={`px-2 py-1 rounded text-xs font-semibold ${ACAO_COLORS[log.acao] || 'bg-gray-100'}`}>
                        {log.acao}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-sm">{log.usuario_login}</td>
                    <td className="px-4 py-3 text-sm text-gray-600">{log.entidade || '-'}</td>
                    <td className="px-4 py-3 text-sm text-gray-600">{log.objeto_repr || '-'}</td>
                    <td className="px-4 py-3 text-sm text-gray-600">{log.ip || '-'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Modal de Detalhes */}
      {selectedLog && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold">Detalhes do Evento</h2>
                <button
                  onClick={() => setSelectedLog(null)}
                  className="text-gray-500 hover:text-gray-700 text-2xl"
                >
                  ×
                </button>
              </div>

              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold text-gray-700">Data/Hora</label>
                    <p className="text-gray-900">
                      {new Date(selectedLog.data_hora).toLocaleString('pt-BR')}
                    </p>
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700">Ação</label>
                    <p className="text-gray-900">
                      <span className={`px-2 py-1 rounded text-sm font-semibold ${ACAO_COLORS[selectedLog.acao]}`}>
                        {selectedLog.acao}
                      </span>
                    </p>
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700">Usuário</label>
                    <p className="text-gray-900">{selectedLog.usuario_login}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700">Perfil</label>
                    <p className="text-gray-900">{selectedLog.perfil || '-'}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700">Entidade</label>
                    <p className="text-gray-900">{selectedLog.entidade || '-'}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700">Objeto ID</label>
                    <p className="text-gray-900 font-mono text-sm">{selectedLog.objeto_id || '-'}</p>
                  </div>
                  <div className="col-span-2">
                    <label className="block text-sm font-semibold text-gray-700">Representação</label>
                    <p className="text-gray-900">{selectedLog.objeto_repr || '-'}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700">IP</label>
                    <p className="text-gray-900">{selectedLog.ip || '-'}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700">Método HTTP</label>
                    <p className="text-gray-900">{selectedLog.metodo_http || '-'}</p>
                  </div>
                  <div className="col-span-2">
                    <label className="block text-sm font-semibold text-gray-700">Caminho</label>
                    <p className="text-gray-900 font-mono text-sm">{selectedLog.caminho || '-'}</p>
                  </div>
                  <div className="col-span-2">
                    <label className="block text-sm font-semibold text-gray-700">User Agent</label>
                    <p className="text-gray-900 text-xs break-words">{selectedLog.user_agent || '-'}</p>
                  </div>
                </div>

                {/* Alterações (diff para UPDATE, snapshot para CREATE) */}
                {selectedLog.alteracoes && (
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Alterações</label>
                    <pre className="bg-gray-50 p-4 rounded border text-xs overflow-auto max-h-64">
                      {JSON.stringify(selectedLog.alteracoes, null, 2)}
                    </pre>
                  </div>
                )}
              </div>

              <div className="mt-6 flex justify-end">
                <button
                  onClick={() => setSelectedLog(null)}
                  className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
                >
                  Fechar
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AuditoriaPage;
