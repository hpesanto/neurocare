import { NavLink } from "react-router-dom";

interface MenuItem {
  label: string;
  path: string;
}

interface MenuSection {
  title: string;
  items: MenuItem[];
}

const MENU: MenuSection[] = [
  {
    title: "Cadastro",
    items: [
      { label: "Pacientes", path: "/cadastro/pacientes" },
      { label: "Profissionais", path: "/cadastro/profissionais" },
      { label: "Convênios", path: "/cadastro/convenios" },
      { label: "Formas de Pagamento", path: "/cadastro/formas-pagamento" },
      { label: "Tipos de Produto", path: "/cadastro/tipos-produto" },
      { label: "Produtos", path: "/cadastro/produtos" },
      { label: "Faixas Etárias", path: "/cadastro/faixas-etarias" },
      { label: "Tipos de Serviço", path: "/cadastro/tipos-servico" },
      { label: "Contatos de Emergência", path: "/cadastro/contatos-emergencia" },
    ],
  },
  {
    title: "Atendimento",
    items: [
      { label: "Evolução Clínica", path: "/atendimento/evolucao-clinica" },
      { label: "Avaliação Neuropsicológica", path: "/atendimento/avaliacao-neuropsicologica" },
      { label: "Reabilitação - Objetivos", path: "/atendimento/objetivos-reabilitacao" },
      { label: "Reabilitação - Sessões", path: "/atendimento/sessoes-reabilitacao" },
    ],
  },
  {
    title: "Financeiro",
    items: [
      { label: "Reabilitação Neuropsicológica", path: "/financeiro/reabilitacao" },
      { label: "Transações", path: "/financeiro/transacoes" },
      { label: "Tipos de Transação", path: "/financeiro/tipos-transacao" },
      { label: "Status de Pagamento", path: "/financeiro/status-pagamento" },
    ],
  },
  {
    title: "Vendas",
    items: [
      { label: "Vendas Vinculadas", path: "/vendas/vinculadas" },
      { label: "Vendas Gerais", path: "/vendas/geral" },
    ],
  },
];

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2>NeuroCare</h2>
      </div>
      <nav>
        {MENU.map((section) => (
          <div key={section.title} className="menu-section">
            <h3>{section.title}</h3>
            <ul>
              {section.items.map((item) => (
                <li key={item.path}>
                  <NavLink to={item.path}>{item.label}</NavLink>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </nav>
    </aside>
  );
}
