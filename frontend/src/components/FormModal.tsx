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

const FIELD_LABELS: Record<string, string> = {
  nome_completo: "Nome Completo",
  data_nascimento: "Data de Nascimento",
  telefone_principal: "Telefone Principal",
  id_paciente: "Paciente",
  id_psicologo: "Psicologo",
  id_psicologo_responsavel: "Psicologo Responsavel",
  id_convenio: "Convenio",
  id_faixa_etaria: "Faixa Etaria",
  id_tipo_produto: "Tipo de Produto",
  id_tipo_servico: "Tipo de Servico",
  id_tipo_transacao: "Tipo de Transacao",
  id_forma_pagamento: "Forma de Pagamento",
  id_status_pagamento: "Status de Pagamento",
  id_forma_cobranca: "Forma de Cobranca",
  id_perfil_acesso: "Perfil de Acesso",
  id_reabilitacao: "Reabilitacao",
  id_produto: "Produto",
  id_venda_geral: "Venda Geral",
  id_status_objetivo: "Status do Objetivo",
  data_sessao: "Data da Sessao",
  data_avaliacao: "Data da Avaliacao",
  data_inicio: "Data de Inicio",
  data_transacao: "Data da Transacao",
  data_venda: "Data da Venda",
  evolucao_texto: "Evolucao",
  motivo_avaliacao: "Motivo da Avaliacao",
  programa_descricao: "Descricao do Programa",
  passos_realizados: "Passos Realizados",
  valor: "Valor",
  valor_unitario: "Valor Unitario",
  valor_total_produto: "Valor Total",
  valor_total_transacao: "Valor Total",
  valor_total_item: "Valor Total do Item",
  quantidade: "Quantidade",
  descricao: "Descricao",
  nome: "Nome",
  nome_contato: "Nome do Contato",
  telefone_contato: "Telefone",
  parentesco: "Parentesco",
  email: "Email",
  login: "Login",
  senha: "Senha",
  cpf: "CPF",
};

function formatErrors(data: unknown): string[] {
  if (typeof data === "string") return [data];
  if (Array.isArray(data)) return data.map(String);
  if (data && typeof data === "object") {
    const errors: string[] = [];
    for (const [field, msgs] of Object.entries(data as Record<string, unknown>)) {
      const label = FIELD_LABELS[field] || field.replace(/_/g, " ");
      const msgList = Array.isArray(msgs) ? msgs : [msgs];
      for (const msg of msgList) {
        errors.push(`${label}: ${String(msg)}`);
      }
    }
    return errors;
  }
  return ["Erro ao salvar. Verifique os campos e tente novamente."];
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
  const [errors, setErrors] = useState<string[]>([]);

  useEffect(() => {
    if (open) setErrors([]);
  }, [open]);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setErrors([]);
    try {
      const formData = new FormData(e.currentTarget);
      const data: Record<string, string> = {};
      formData.forEach((value, key) => {
        data[key] = value as string;
      });
      await onSubmit(data);
      onClose();
    } catch (err: unknown) {
      if (err && typeof err === "object" && "response" in err) {
        const respData = (err as { response: { data: unknown } }).response.data;
        setErrors(formatErrors(respData));
      } else {
        setErrors(["Erro ao salvar. Verifique sua conexao e tente novamente."]);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal show={open} onHide={onClose} size={size} centered backdrop="static" keyboard={false}>
      <form onSubmit={handleSubmit}>
        <Modal.Header closeButton className="border-bottom">
          <Modal.Title as="h5">{title}</Modal.Title>
        </Modal.Header>
        <Modal.Body>{children}</Modal.Body>
        {errors.length > 0 && (
          <Alert variant="danger" className="mx-3 mb-0" dismissible onClose={() => setErrors([])}>
            <Alert.Heading as="h6" className="mb-1">
              <i className="bi bi-exclamation-triangle me-1" />
              Corrija os erros abaixo:
            </Alert.Heading>
            <ul className="mb-0 ps-3">
              {errors.map((e, i) => (
                <li key={i}>{e}</li>
              ))}
            </ul>
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
