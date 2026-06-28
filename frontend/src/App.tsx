import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AuthProvider } from "./auth/AuthContext";
import ProtectedRoute from "./auth/ProtectedRoute";
import LoginPage from "./auth/LoginPage";
import MainLayout from "./components/Layout/MainLayout";
import LookupCrudPage from "./pages/LookupCrudPage";
import PacientesPage from "./pages/cadastro/PacientesPage";
import ProfissionaisPage from "./pages/cadastro/ProfissionaisPage";
import ProdutosPage from "./pages/cadastro/ProdutosPage";
import ContatosEmergenciaPage from "./pages/cadastro/ContatosEmergenciaPage";
import EvolucaoClinicaPage from "./pages/atendimento/EvolucaoClinicaPage";
import AvaliacaoPage from "./pages/atendimento/AvaliacaoPage";
import ObjetivosReabPage from "./pages/atendimento/ObjetivosReabPage";
import SessoesReabPage from "./pages/atendimento/SessoesReabPage";
import ReabilitacaoPage from "./pages/atendimento/ReabilitacaoPage";
import PacienteServicoPage from "./pages/cadastro/PacienteServicoPage";
import PacienteDetailPage from "./pages/cadastro/PacienteDetailPage";
import TransacoesPage from "./pages/financeiro/TransacoesPage";
import VendasVinculadasPage from "./pages/vendas/VendasVinculadasPage";
import VendasGeralPage from "./pages/vendas/VendasGeralPage";
import CalendarPage from "./pages/agendamento/CalendarPage";
import AuditoriaPage from "./pages/admin/AuditoriaPage";
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
              <Route index element={<Navigate to="/agendamento" replace />} />

              {/* Agendamento */}
              <Route path="agendamento" element={<CalendarPage />} />

              {/* Cadastro */}
              <Route path="cadastro/pacientes" element={<PacientesPage />} />
              <Route path="cadastro/pacientes/:id" element={<PacienteDetailPage />} />
              <Route path="cadastro/profissionais" element={<ProfissionaisPage />} />
              <Route path="cadastro/convenios" element={<LookupCrudPage endpoint={ENDPOINTS.convenios} title="Convenios" itemLabel="Convenio" />} />
              <Route path="cadastro/formas-pagamento" element={<LookupCrudPage endpoint={ENDPOINTS.formasPagamento} title="Formas de Pagamento" itemLabel="Forma de Pagamento" />} />
              <Route path="cadastro/tipos-produto" element={<LookupCrudPage endpoint={ENDPOINTS.tiposProduto} title="Tipos de Produto" itemLabel="Tipo de Produto" />} />
              <Route path="cadastro/produtos" element={<ProdutosPage />} />
              <Route path="cadastro/faixas-etarias" element={<LookupCrudPage endpoint={ENDPOINTS.faixasEtarias} title="Faixas Etarias" itemLabel="Faixa Etaria" />} />
              <Route path="cadastro/tipos-servico" element={<LookupCrudPage endpoint={ENDPOINTS.tiposServico} title="Tipos de Servico" itemLabel="Tipo de Servico" />} />
              <Route path="cadastro/contatos-emergencia" element={<ContatosEmergenciaPage />} />
              <Route path="cadastro/paciente-servico" element={<PacienteServicoPage />} />

              {/* Atendimento */}
              <Route path="atendimento/evolucao-clinica" element={<EvolucaoClinicaPage />} />
              <Route path="atendimento/avaliacao-neuropsicologica" element={<AvaliacaoPage />} />
              <Route path="atendimento/objetivos-reabilitacao" element={<ObjetivosReabPage />} />
              <Route path="atendimento/sessoes-reabilitacao" element={<SessoesReabPage />} />

              {/* Financeiro */}
              <Route path="financeiro/reabilitacao" element={<ReabilitacaoPage />} />
              <Route path="financeiro/transacoes" element={<TransacoesPage />} />
              <Route path="financeiro/tipos-transacao" element={<LookupCrudPage endpoint={ENDPOINTS.tiposTransacao} title="Tipos de Transacao" itemLabel="Tipo de Transacao" />} />
              <Route path="financeiro/status-pagamento" element={<LookupCrudPage endpoint={ENDPOINTS.statusPagamento} title="Status de Pagamento" itemLabel="Status" />} />
              <Route path="financeiro/formas-cobranca" element={<LookupCrudPage endpoint={ENDPOINTS.formasCobrancaReabilitacao} title="Formas de Cobranca" itemLabel="Forma de Cobranca" />} />
              <Route path="financeiro/status-objetivo" element={<LookupCrudPage endpoint={ENDPOINTS.statusObjetivoReabilitacao} title="Status de Objetivo" itemLabel="Status" />} />

              {/* Vendas */}
              <Route path="vendas/vinculadas" element={<VendasVinculadasPage />} />
              <Route path="vendas/geral" element={<VendasGeralPage />} />

              {/* Admin */}
              <Route path="auditoria" element={<AuditoriaPage />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  );
}
