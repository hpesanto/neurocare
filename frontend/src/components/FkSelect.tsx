import { Form, Spinner } from "react-bootstrap";
import { useOptions } from "../hooks/useOptions";

interface FkSelectProps {
  name: string;
  label: string;
  endpoint: string;
  labelField?: string;
  defaultValue?: string | null;
  required?: boolean;
}

export default function FkSelect({
  name,
  label,
  endpoint,
  labelField = "nome",
  defaultValue,
  required = false,
}: FkSelectProps) {
  const { options, isLoading } = useOptions(endpoint, labelField);

  return (
    <Form.Group>
      <Form.Label>
        {label} {required && "*"}
        {isLoading && <Spinner animation="border" size="sm" className="ms-1" />}
      </Form.Label>
      <Form.Select name={name} defaultValue={defaultValue ?? ""} required={required}>
        <option value="">Selecione...</option>
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </Form.Select>
    </Form.Group>
  );
}
