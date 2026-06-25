import { useState } from "react";

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

  if (isLoading) return <div className="loading">Carregando...</div>;

  return (
    <div className="data-table-container">
      <div className="data-table-header">
        <h2>{title}</h2>
        <div className="data-table-actions">
          <input
            type="text"
            placeholder="Buscar..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="search-input"
          />
          {onAdd && (
            <button onClick={onAdd} className="btn-primary">
              + Novo
            </button>
          )}
        </div>
      </div>
      <table className="data-table">
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={String(col.key)}>{col.label}</th>
            ))}
            {(onEdit || onDelete) && <th>Ações</th>}
          </tr>
        </thead>
        <tbody>
          {filtered.map((item) => (
            <tr key={item.id}>
              {columns.map((col) => (
                <td key={String(col.key)}>
                  {col.render
                    ? col.render(item)
                    : String((item as Record<string, unknown>)[col.key as string] ?? "")}
                </td>
              ))}
              {(onEdit || onDelete) && (
                <td className="actions-cell">
                  {onEdit && (
                    <button onClick={() => onEdit(item)} className="btn-edit">
                      Editar
                    </button>
                  )}
                  {onDelete && (
                    <button onClick={() => onDelete(item.id)} className="btn-delete">
                      Excluir
                    </button>
                  )}
                </td>
              )}
            </tr>
          ))}
          {filtered.length === 0 && (
            <tr>
              <td colSpan={columns.length + 1} className="empty-row">
                Nenhum registro encontrado
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
