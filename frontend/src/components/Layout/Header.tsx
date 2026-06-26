import { Button, Container, Dropdown, Navbar } from "react-bootstrap";
import { useAuth } from "../../auth/AuthContext";

export default function Header() {
  const { user, logout } = useAuth();

  return (
    <Navbar bg="white" className="border-bottom shadow-sm px-3">
      <Container fluid>
        <Navbar.Text className="fw-semibold text-dark">
          Sistema de Gestao Clinica
        </Navbar.Text>
        <div className="d-flex align-items-center">
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
