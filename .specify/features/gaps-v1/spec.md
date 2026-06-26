# NeuroCare — Gaps da Especificacao v1

## Contexto
Validacao da aplicacao contra o documento "Espec_NeuroCare_2025.docx".
A aplicacao cobre 75% dos requisitos. Este plano endereca os 7 gaps identificados.

## Requisitos pendentes (por prioridade)

### P1 — Controle de acesso por perfil
- Perfil Secretaria: ve cadastro, sem financeiro/evolucao
- Perfil Psicologa: so seus proprios pacientes e dados financeiros
- Perfil Admin: acesso total
- Modulo 5 inteiro da especificacao

### P2 — Relatorios financeiros com exportacao
- Exportacao CSV/Excel por periodo, psicologo, tipo
- Dados para o contador: data, valor, tipo servico/produto, CPF, endereco, email

### P3 — Isolamento de dados por psicologo
- Psicologa so ve pacientes onde ela eh psicologo_responsavel
- Financeiro filtrado por psicologo logado

### P4 — Upload de laudo PDF
- Campo caminho_laudo_pdf existe no model
- Falta endpoint de upload e armazenamento

### P5 — Vinculacao automatica vendas -> transacoes
- Ao criar venda vinculada ou geral, criar transacao financeira automaticamente

### P6 — Abas de tratamento integradas ao perfil do paciente
- PacienteServico existe mas nao esta integrado ao perfil
- Especificacao pede ativar/desativar areas por paciente

### P7 — Filtros avancados na UI
- API ja suporta filtros via query params
- UI precisa de componentes de filtro (data range, selects)
