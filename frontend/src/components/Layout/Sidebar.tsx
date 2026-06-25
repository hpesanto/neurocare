import { Nav } from "react-bootstrap";
import { NavLink } from "react-router-dom";

interface MenuItem {
  label: string;
  path: string;
  icon: string;
}

interface MenuSection {
  title: string;
  items: MenuItem[];
}

const MENU: MenuSection[] = [
  {
    title: "Cadastro",
    items: [
      { label: "Pacientes", path: "/cadastro/pacientes", icon: "bi-people" },
      { label: "Profissionais", path: "/cadastro/profissionais", icon: "bi-person-badge" },
      { label: "Convenios", path: "/cadastro/convenios", icon: "bi-building" },
      { label: "Formas de Pagamento", path: "/cadastro/formas-pagamento", icon: "bi-credit-card" },
      { label: "Tipos de Produto", path: "/cadastro/tipos-produto", icon: "bi-tags" },
      { label: "Produtos", path: "/cadastro/produtos", icon: "bi-box" },
      { label: "Faixas Etarias", path: "/cadastro/faixas-etarias", icon: "bi-bar-chart-steps" },
      { label: "Tipos de Servico", path: "/cadastro/tipos-servico", icon: "bi-gear" },
      { label: "Contatos Emergencia", path: "/cadastro/contatos-emergencia", icon: "bi-telephone" },
    ],
  },
  {
    title: "Atendimento",
    items: [
      { label: "Evolucao Clinica", path: "/atendimento/evolucao-clinica", icon: "bi-journal-medical" },
      { label: "Avaliacao Neuropsi.", path: "/atendimento/avaliacao-neuropsicologica", icon: "bi-clipboard2-pulse" },
      { label: "Objetivos Reab.", path: "/atendimento/objetivos-reabilitacao", icon: "bi-bullseye" },
      { label: "Sessoes Reab.", path: "/atendimento/sessoes-reabilitacao", icon: "bi-calendar-check" },
    ],
  },
  {
    title: "Financeiro",
    items: [
      { label: "Reabilitacao", path: "/financeiro/reabilitacao", icon: "bi-heart-pulse" },
      { label: "Transacoes", path: "/financeiro/transacoes", icon: "bi-cash-stack" },
      { label: "Tipos de Transacao", path: "/financeiro/tipos-transacao", icon: "bi-list-check" },
      { label: "Status Pagamento", path: "/financeiro/status-pagamento", icon: "bi-check-circle" },
      { label: "Formas Cobranca", path: "/financeiro/formas-cobranca", icon: "bi-receipt" },
    ],
  },
  {
    title: "Vendas",
    items: [
      { label: "Vendas Vinculadas", path: "/vendas/vinculadas", icon: "bi-cart" },
      { label: "Vendas Gerais", path: "/vendas/geral", icon: "bi-shop" },
    ],
  },
];

export default function Sidebar() {
  return (
    <aside className="nc-sidebar d-flex flex-column">
      <div className="px-3 py-3 border-bottom border-dark">
        <h5 className="text-white mb-0 fw-bold">
          <i className="bi bi-activity me-2" />
          NeuroCare
        </h5>
      </div>
      <Nav className="flex-column py-2 flex-grow-1">
        {MENU.map((section) => (
          <div key={section.title}>
            <div className="nc-section-label">{section.title}</div>
            {section.items.map((item) => (
              <Nav.Link
                key={item.path}
                as={NavLink}
                to={item.path}
                className="d-flex align-items-center gap-2"
              >
                <i className={`bi ${item.icon}`} />
                {item.label}
              </Nav.Link>
            ))}
          </div>
        ))}
      </Nav>
      <div className="px-3 py-3 border-top border-dark">
        <small className="text-white-50">NeuroCare v2.0</small>
      </div>
    </aside>
  );
}
