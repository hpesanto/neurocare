import { useState, type FormEvent } from "react";
import { Alert, Button, Card, Form, Spinner } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import { useAuth } from "./AuthContext";

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(username, password);
      navigate("/");
    } catch {
      setError("Usuario ou senha invalidos");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="nc-login-bg d-flex align-items-center justify-content-center">
      <Card className="nc-login-card shadow-lg border-0">
        <Card.Body className="p-5">
          <div className="text-center mb-4">
            <img src="/logo.jpg" alt="NeuroCare" style={{ width: 80, height: 80, borderRadius: 8 }} />
            <h3 className="fw-bold mt-2" style={{ color: "#1a3c40" }}>NeuroCare</h3>
            <p className="text-muted small">Consultorios Integrados</p>
          </div>
          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3">
              <Form.Label>Usuario</Form.Label>
              <div className="input-group">
                <span className="input-group-text">
                  <i className="bi bi-person" />
                </span>
                <Form.Control
                  type="text"
                  placeholder="Digite seu usuario"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                  autoFocus
                />
              </div>
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Senha</Form.Label>
              <div className="input-group">
                <span className="input-group-text">
                  <i className="bi bi-lock" />
                </span>
                <Form.Control
                  type="password"
                  placeholder="Digite sua senha"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
            </Form.Group>
            {error && <Alert variant="danger" className="py-2">{error}</Alert>}
            <Button variant="primary" type="submit" className="w-100 mt-2" disabled={loading}>
              {loading ? (
                <Spinner animation="border" size="sm" />
              ) : (
                <>
                  <i className="bi bi-box-arrow-in-right me-2" />
                  Entrar
                </>
              )}
            </Button>
          </Form>
        </Card.Body>
      </Card>
    </div>
  );
}
