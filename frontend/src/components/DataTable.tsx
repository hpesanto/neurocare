import { useState } from "react";
import { Badge, Button, Card, Form, InputGroup, Spinner, Table } from "react-bootstrap";

interface Column<T> {
  key: keyof T | string;
  label: string;
  render?: (item: T) => React.ReactNode;
}

interface DataTableProps<T extends { id: string }> {
  columns: Column<T>[];
  items: T[];
  isLoading: boolean;
  onEdit?: (item: T) => void;
  onDelete?: (id: string) => void;
  title: string;
  onAdd?: () => void;
}

export default function DataTable<T extends { id: string }>({
  columns,
  items,
  isLoading,
  onEdit,
  onDelete,
  title,
  onAdd,
}: DataTableProps<T>) {
  const [search, setSearch] = useState("");

  const filtered = items.filter((item) =>
    columns.some((col) => {
      const val = (item as Record<string, unknown>)[col.key as string];
      return val && String(val).toLowerCase().includes(search.toLowerCase());
    })
  );

  return (
    <Card>
      <Card.Header className="bg-white py-3">
        <div className="d-flex justify-content-between align-items-center">
          <div className="d-flex align-items-center gap-2">
            <h5 className="mb-0 fw-bold">{title}</h5>
            <Badge bg="secondary" pill>
              {filtered.length}
            </Badge>
          </div>
          <div className="d-flex gap-2 align-items-center">
            <InputGroup size="sm" style={{ width: 250 }}>
              <InputGroup.Text>
                <i className="bi bi-search" />
              </InputGroup.Text>
              <Form.Control
                placeholder="Buscar..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </InputGroup>
            {onAdd && (
              <Button size="sm" onClick={onAdd}>
                <i className="bi bi-plus-lg me-1" />
                Novo
              </Button>
            )}
          </div>
        </div>
      </Card.Header>
      <Card.Body className="p-0">
        {isLoading ? (
          <div className="text-center py-5">
            <Spinner animation="border" variant="primary" />
          </div>
        ) : (
          <Table hover responsive className="mb-0">
            <thead className="table-light">
              <tr>
                {columns.map((col) => (
                  <th key={String(col.key)}>{col.label}</th>
                ))}
                {(onEdit || onDelete) && <th style={{ width: 120 }}>Acoes</th>}
              </tr>
            </thead>
            <tbody>
              {filtered.map((item) => (
                <tr key={item.id}>
                  {columns.map((col) => (
                    <td key={String(col.key)}>
                      {col.render
                        ? col.render(item)
                        : String((item as Record<string, unknown>)[col.key as string] ?? "—")}
                    </td>
                  ))}
                  {(onEdit || onDelete) && (
                    <td>
                      <div className="d-flex gap-1">
                        {onEdit && (
                          <Button
                            variant="outline-primary"
                            size="sm"
                            onClick={() => onEdit(item)}
                            title="Editar"
                          >
                            <i className="bi bi-pencil" />
                          </Button>
                        )}
                        {onDelete && (
                          <Button
                            variant="outline-danger"
                            size="sm"
                            onClick={() => onDelete(item.id)}
                            title="Excluir"
                          >
                            <i className="bi bi-trash" />
                          </Button>
                        )}
                      </div>
                    </td>
                  )}
                </tr>
              ))}
              {filtered.length === 0 && (
                <tr>
                  <td colSpan={columns.length + 1} className="text-center text-muted py-4">
                    <i className="bi bi-inbox fs-3 d-block mb-2" />
                    Nenhum registro encontrado
                  </td>
                </tr>
              )}
            </tbody>
          </Table>
        )}
      </Card.Body>
    </Card>
  );
}
