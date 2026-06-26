# Quickstart — Validacao dos Gaps

## Pre-requisitos
- Docker Compose rodando (`docker compose up --build`)
- Login: admin / admin123

## Cenarios de validacao

### 1. Controle de acesso por perfil
```bash
# Criar usuarios com perfis diferentes
POST /api/profissionais/ — perfil "Secretaria"
POST /api/profissionais/ — perfil "Psicologo"

# Logar como secretaria
POST /api/token/ {"username":"secretaria","password":"..."}

# Tentar acessar evolucao clinica — deve retornar 403
GET /api/evolucao-clinica/

# Tentar acessar transacoes — deve retornar 403
GET /api/transacoes/
```

### 2. Isolamento por psicologo
```bash
# Logar como Dra. Mariana
# Listar pacientes — deve retornar APENAS seus pacientes
GET /api/pacientes/
# Verificar que nao ve pacientes de outra psicologa
```

### 3. Exportacao financeira
```bash
# Exportar CSV
GET /api/transacoes/exportar/?formato=csv&data_inicio=2026-01-01&data_fim=2026-12-31
# Verificar headers: data, valor, tipo, CPF, endereco, email

# Exportar Excel
GET /api/transacoes/exportar/?formato=xlsx&data_inicio=2026-06-01
```

### 4. Upload de laudo
```bash
# Upload PDF na avaliacao
PATCH /api/avaliacao-neuropsicologica/{id}/
Content-Type: multipart/form-data
file: laudo.pdf
```

### 5. Auto-criacao de transacao
```bash
# Criar venda vinculada
POST /api/vendas-vinculadas/ {...}
# Verificar que transacao foi criada automaticamente
GET /api/transacoes/?id_venda_vinculada_paciente={venda_id}
```

### 6. Filtros na UI
- Abrir /financeiro/transacoes no browser
- Verificar filtros de data, psicologo, tipo de transacao
- Testar combinacao de filtros
```

### 7. Perfil do paciente com abas
- Abrir /cadastro/pacientes no browser
- Clicar em um paciente
- Verificar abas: Dados, Evolucao, Avaliacao, Reabilitacao, Vendas
