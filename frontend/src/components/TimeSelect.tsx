import { Form } from "react-bootstrap";

const TIME_OPTIONS: string[] = [];
for (let h = 0; h < 24; h++) {
  for (const m of [0, 30]) {
    TIME_OPTIONS.push(`${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}`);
  }
}

interface TimeSelectProps {
  name: string;
  label: string;
  defaultValue?: string | null;
  required?: boolean;
}

export default function TimeSelect({ name, label, defaultValue, required }: TimeSelectProps) {
  const normalized = defaultValue?.slice(0, 5) ?? "";

  return (
    <Form.Group>
      <Form.Label>{label}</Form.Label>
      <Form.Select name={name} defaultValue={normalized} required={required}>
        <option value="">Selecione...</option>
        {TIME_OPTIONS.map((t) => (
          <option key={t} value={t}>{t}</option>
        ))}
      </Form.Select>
    </Form.Group>
  );
}
