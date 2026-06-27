import { useState } from "react";
import { Button, Modal } from "react-bootstrap";
import { useLocation } from "react-router-dom";
import { getHelpDoc } from "../docs";
import Markdown from "./Markdown";

// Botão de ajuda exibido no cabeçalho. Mostra, em um modal, a documentação
// da tela atual (resolvida a partir da rota). Some quando não há doc para a rota.
export default function HelpButton() {
  const { pathname } = useLocation();
  const [open, setOpen] = useState(false);
  const doc = getHelpDoc(pathname);

  if (!doc) return null;

  return (
    <>
      <Button
        variant="light"
        size="sm"
        className="d-flex align-items-center gap-1 border"
        onClick={() => setOpen(true)}
        title="Ajuda desta tela"
      >
        <i className="bi bi-question-circle" />
        Ajuda
      </Button>

      <Modal show={open} onHide={() => setOpen(false)} size="lg" scrollable centered>
        <Modal.Header closeButton>
          <Modal.Title as="h5">
            <i className="bi bi-question-circle me-2" />
            Ajuda
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Markdown content={doc} />
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setOpen(false)}>
            Fechar
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}
