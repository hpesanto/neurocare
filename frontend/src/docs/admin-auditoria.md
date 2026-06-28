# Log de Auditoria

Visualize, filtre e exporte todos os eventos de auditoria do sistema.

## O que é rastreado

- **Autenticação**: login com sucesso, falhas de login, logout
- **Dados**: criação, alteração e exclusão de registros
- **Leitura**: visualização de prontuários (pacientes e documentos clínicos)

Cada evento registra:
- Quem (usuário + perfil)
- Quando (data/hora precisa)
- O quê (entidade, ID do registro)
- O que mudou (diferença antes/depois)
- De onde (IP, navegador, requisição)

## Como usar

### Filtros

Use os filtros para localizar eventos específicos:

- **Ação**: filtrar por tipo de evento (login, criar, alterar, etc.)
- **Entidade**: filtrar por tipo de registro afetado (Paciente, Evolução, etc.)
- **Usuário**: buscar por nome de usuário
- **Período**: filtrar por data de início e fim

### Visualizar detalhes

Clique em qualquer linha da tabela para abrir um modal com detalhes completos, incluindo:
- Campos que foram alterados (se for um UPDATE)
- Valores antes e depois
- IP e User-Agent

### Exportar

Exporte os logs filtrados em:
- **CSV**: para planilhas
- **XLSX**: para Excel

## Permissões

Apenas administradores podem acessar o log de auditoria. Se você não vê esta página, verifique suas permissões.

## Conformidade LGPD

O registro de leitura (visualização de prontuários) é uma exigência LGPD. Todos os acessos a documentos clínicos são auditados automaticamente.

Campos sensíveis (senhas, tokens) **nunca** são registrados nos logs.
