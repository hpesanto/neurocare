import { useAuth } from "../../auth/AuthContext";

export default function Header() {
  const { user, logout } = useAuth();

  return (
    <header className="header">
      <div className="header-title">Sistema de Gestão Clínica</div>
      <div className="header-user">
        <span>{user?.first_name || user?.username}</span>
        <button onClick={logout} className="btn-logout">
          Sair
        </button>
      </div>
    </header>
  );
}
