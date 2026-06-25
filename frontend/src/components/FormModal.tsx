import { useEffect, useState, type FormEvent, type ReactNode } from "react";
import { Alert, Button, Modal, Spinner } from "react-bootstrap";

interface FormModalProps {
  title: string;
  open: boolean;
  onClose: () => void;
  onSubmit: (data: Record<string, string>) => Promise<void>;
  initialData?: Record<string, string>;
  children: ReactNode;
  size?: "sm" | "lg" | "xl";
}

export default function FormModal({
  title,
  open,
  onClose,
  onSubmit,
  children,
  size = "lg",
}: FormModalProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (open) setError("");
  }, [open]);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const formData = new FormData(e.currentTarget);
      const data: Record<string, string> = {};
      formData.forEach((value, key) => {
        data[key] = value as string;
      });
      await onSubmit(data);
      onClose();
    } catch (err: unknown) {
      const msg =
        err && typeof err === "object" && "response" in err
          ? JSON.stringify((err as { response: { data: unknown } }).response.data)
          : "Erro ao salvar";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal show={open} onHide={onClose} size={size} centered>
      <form onSubmit={handleSubmit}>
        <Modal.Header closeButton className="border-bottom">
          <Modal.Title as="h5">{title}</Modal.Title>
        </Modal.Header>
        <Modal.Body>{children}</Modal.Body>
        {error && (
          <Alert variant="danger" className="mx-3 mb-0" dismissible onClose={() => setError("")}>
            {error}
          </Alert>
        )}
        <Modal.Footer className="border-top">
          <Button variant="secondary" onClick={onClose} disabled={loading}>
            Cancelar
          </Button>
          <Button variant="primary" type="submit" disabled={loading}>
            {loading ? (
              <>
                <Spinner animation="border" size="sm" className="me-2" />
                Salvando...
              </>
            ) : (
              <>
                <i className="bi bi-check-lg me-1" />
                Salvar
              </>
            )}
          </Button>
        </Modal.Footer>
      </form>
    </Modal>
  );
}
