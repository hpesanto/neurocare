import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AuthProvider } from "./auth/AuthContext";
import ProtectedRoute from "./auth/ProtectedRoute";
import LoginPage from "./auth/LoginPage";
import MainLayout from "./components/Layout/MainLayout";
import LookupCrudPage from "./pages/LookupCrudPage";
import PacientesPage from "./pages/cadastro/PacientesPage";
import { ENDPOINTS } from "./api/endpoints";

const queryClient = new QueryClient({
  defaultOptions: { queries: { staleTime: 30_000 } },
});

function ProtectedApp() {
  return (
    <ProtectedRoute>
      <MainLayout />
    </ProtectedRoute>
  );
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route element={<ProtectedApp />}>
              <Route index element={<Navigate to="/cadastro/pacientes" replace />} />

              {/* Cadastro */}
              <Route path="cadastro/pacientes" element={<PacientesPage />} />
              <Route path="cadastro/convenios" element={<LookupCrudPage endpoint={ENDPOINTS.convenios} title="Convênios" itemLabel="Convênio" />} />
              <Route path="cadastro/formas-pagamento" element={<LookupCrudPage endpoint={ENDPOINTS.formasPagamento} title="Formas de Pagamento" itemLabel="Forma de Pagamento" />} />
              <Route path="cadastro/tipos-produto" element={<LookupCrudPage endpoint={ENDPOINTS.tiposProduto} title="Tipos de Produto" itemLabel="Tipo de Produto" />} />
              <Route path="cadastro/faixas-etarias" element={<LookupCrudPage endpoint={ENDPOINTS.faixasEtarias} title="Faixas Etárias" itemLabel="Faixa Etária" />} />
              <Route path="cadastro/tipos-servico" element={<LookupCrudPage endpoint={ENDPOINTS.tiposServico} title="Tipos de Serviço" itemLabel="Tipo de Serviço" />} />

              {/* Atendimento */}
              <Route path="atendimento/evolucao-clinica" element={<LookupCrudPage endpoint={ENDPOINTS.evolucaoClinica} title="Evolução Clínica" itemLabel="Evolução" />} />

              {/* Financeiro */}
              <Route path="financeiro/tipos-transacao" element={<LookupCrudPage endpoint={ENDPOINTS.tiposTransacao} title="Tipos de Transação" itemLabel="Tipo de Transação" />} />
              <Route path="financeiro/status-pagamento" element={<LookupCrudPage endpoint={ENDPOINTS.statusPagamento} title="Status de Pagamento" itemLabel="Status" />} />
              <Route path="financeiro/formas-cobranca" element={<LookupCrudPage endpoint={ENDPOINTS.formasCobrancaReabilitacao} title="Formas de Cobrança" itemLabel="Forma de Cobrança" />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  );
}
