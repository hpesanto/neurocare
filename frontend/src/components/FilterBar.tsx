import { useState } from "react";
import { Button, Card, Col, Form, Row } from "react-bootstrap";
import FkSelect from "./FkSelect";

export interface FilterField {
  name: string;
  label: string;
  type: "date" | "fk-select" | "select";
  endpoint?: string;
  labelField?: string;
  options?: { value: string; label: string }[];
}

interface FilterBarProps {
  fields: FilterField[];
  onApply: (filters: Record<string, string>) => void;
  onClear: () => void;
}

export default function FilterBar({ fields, onApply, onClear }: FilterBarProps) {
  const [open, setOpen] = useState(false);

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const filters: Record<string, string> = {};
    formData.forEach((v, k) => {
      if (v && String(v).trim()) filters[k] = String(v);
    });
    onApply(filters);
  };

  const handleClear = (e: React.FormEvent<HTMLFormElement>) => {
    e.currentTarget.reset();
    onClear();
  };

  return (
    <div className="mb-3">
      <Button
        variant="outline-secondary"
        size="sm"
        onClick={() => setOpen(!open)}
        className="mb-2"
      >
        <i className={`bi bi-funnel me-1`} />
        Filtros {open ? "▲" : "▼"}
      </Button>
      {open && (
        <Card className="mb-3">
          <Card.Body>
            <form onSubmit={handleSubmit} onReset={handleClear}>
              <Row className="g-3 align-items-end">
                {fields.map((f) => (
                  <Col md={3} key={f.name}>
                    {f.type === "date" && (
                      <Form.Group>
                        <Form.Label className="small">{f.label}</Form.Label>
                        <Form.Control name={f.name} type="date" size="sm" />
                      </Form.Group>
                    )}
                    {f.type === "fk-select" && f.endpoint && (
                      <FkSelect
                        name={f.name}
                        label={f.label}
                        endpoint={f.endpoint}
                        labelField={f.labelField}
                      />
                    )}
                    {f.type === "select" && f.options && (
                      <Form.Group>
                        <Form.Label className="small">{f.label}</Form.Label>
                        <Form.Select name={f.name} size="sm">
                          <option value="">Todos</option>
                          {f.options.map((o) => (
                            <option key={o.value} value={o.value}>{o.label}</option>
                          ))}
                        </Form.Select>
                      </Form.Group>
                    )}
                  </Col>
                ))}
                <Col md="auto" className="d-flex gap-2">
                  <Button type="submit" size="sm" variant="primary">
                    <i className="bi bi-search me-1" /> Aplicar
                  </Button>
                  <Button type="reset" size="sm" variant="outline-secondary">
                    Limpar
                  </Button>
                </Col>
              </Row>
            </form>
          </Card.Body>
        </Card>
      )}
    </div>
  );
}
