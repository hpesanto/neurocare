import { Button, Container, Dropdown, Navbar } from "react-bootstrap";
import { useAuth } from "../../auth/AuthContext";
import HelpButton from "../HelpButton";

export default function Header() {
  const { user, logout } = useAuth();

  return (
    <Navbar bg="white" className="px-3" style={{ borderBottom: "1px solid #dce8e6" }}>
      <Container fluid>
        <Navbar.Text className="fw-semibold" style={{ color: "#1a3c40" }}>
          Sistema de Gestao Clinica
        </Navbar.Text>
        <div className="d-flex align-items-center gap-2">
          <HelpButton />
          <Dropdown align="end">
            <Dropdown.Toggle
              variant="light"
              size="sm"
              className="d-flex align-items-center gap-2 border"
            >
              <i className="bi bi-person-circle" />
              {user?.first_name || user?.username}
            </Dropdown.Toggle>
            <Dropdown.Menu>
              <Dropdown.ItemText>
                <small className="text-muted">{user?.email}</small>
                {user?.perfil && (
                  <div><small className="text-primary fw-semibold">{user.perfil}</small></div>
                )}
              </Dropdown.ItemText>
              <Dropdown.Divider />
              <Dropdown.Item as={Button} variant="link" onClick={logout} className="text-danger">
                <i className="bi bi-box-arrow-right me-2" />
                Sair
              </Dropdown.Item>
            </Dropdown.Menu>
          </Dropdown>
        </div>
      </Container>
    </Navbar>
  );
}
