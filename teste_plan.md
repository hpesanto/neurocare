# Plano de Testes E2E — NeuroCare

**Data de execucao:** 2026-06-26
**Ambiente:** Docker Compose (postgres:16 + Django/Gunicorn + React/nginx)
**Usuario de teste:** admin / admin123

## Como executar

```bash
# 1. Ambiente limpo (reset completo do banco)
docker compose down -v
docker compose up --build -d

# 2. Aguardar ~15 segundos para o backend inicializar

# 3. Rodar o script de teste
pip install requests   # apenas na primeira vez
python tests/test_e2e.py
```

**Script:** [tests/test_e2e.py](tests/test_e2e.py) — executa todos os 66 testes automaticamente e reporta PASS/FAIL.

## Legenda

| Icone | Status |
|-------|--------|
| ⬜ | Nao iniciado |
| 🔄 | Em andamento |
| ✅ | Teste OK |
| ❌ | Teste falhou |

---

## 1. Autenticacao e Perfil

| Status | Teste | Endpoint | Acao | Detalhe |
|--------|-------|----------|------|---------|
| ✅ | Login JWT | `POST /api/token/` | AUTH | admin/admin123 → retorna access + refresh |
| ✅ | Refresh token | `POST /api/token/refresh/` | AUTH | refresh token → novo access |
| ✅ | Perfil usuario | `GET /api/auth/me/` | READ | Retorna id, username, email, perfil="Administrador" |

---

## 2. Cadastro — Tabelas de Referencia

| Status | Teste | Menu | Endpoint | Acao | Dados |
|--------|-------|------|----------|------|-------|
| ✅ | Perfil Acesso INSERT | Cadastro | `POST /api/perfis-acesso/` | INSERT | nome="Supervisor", descricao="Perfil supervisor" |
| ✅ | Perfil Acesso UPDATE | Cadastro | `PATCH /api/perfis-acesso/{id}/` | UPDATE | descricao="Supervisor clinico" |
| ✅ | Convenio INSERT | Cadastro > Convenios | `POST /api/convenios/` | INSERT | nome="NotreDame" |
| ✅ | Convenio UPDATE | Cadastro > Convenios | `PATCH /api/convenios/{id}/` | UPDATE | nome="NotreDame Intermedicina" |
| ✅ | Forma Pagamento INSERT | Cadastro > Formas Pagamento | `POST /api/formas-pagamento/` | INSERT | nome="Deposito" |
| ✅ | Tipo Produto INSERT | Cadastro > Tipos Produto | `POST /api/tipos-produto/` | INSERT | nome="Video Aula" |
| ✅ | Faixa Etaria INSERT | Cadastro > Faixas Etarias | `POST /api/faixas-etarias/` | INSERT | nome="Neonatal", descricao="0-28 dias" |
| ✅ | Tipo Servico INSERT | Cadastro > Tipos Servico | `POST /api/tipos-servico/` | INSERT | nome="Supervisao Clinica" |

---

## 3. Cadastro — Profissionais

| Status | Teste | Menu | Endpoint | Acao | Dados |
|--------|-------|------|----------|------|-------|
| ✅ | Profissional INSERT #1 | Cadastro > Profissionais | `POST /api/profissionais/` | INSERT | Dra. Fernanda Costa, login=fernanda2, perfil=Psicologo |
| ✅ | Profissional INSERT #2 | Cadastro > Profissionais | `POST /api/profissionais/` | INSERT | Dr. Roberto Lima, login=roberto2, perfil=Psicologo |
| ✅ | Profissional INSERT #3 | Cadastro > Profissionais | `POST /api/profissionais/` | INSERT | Dra. Camila Santos, login=camila2, perfil=Psicologo |
| ✅ | Profissional UPDATE | Cadastro > Profissionais | `PATCH /api/profissionais/{id}/` | UPDATE | nome="Dra. Fernanda Costa Silva" |
| ✅ | Login auto-criado | `POST /api/token/` | AUTH | fernanda2/Test@2026 → JWT valido |

---

## 4. Cadastro — Produtos

| Status | Teste | Menu | Endpoint | Acao | Dados |
|--------|-------|------|----------|------|-------|
| ✅ | Produto INSERT | Cadastro > Produtos | `POST /api/produtos/` | INSERT | nome="Video Relaxamento", valor=79.90, tipo="Video Aula" |
| ✅ | Produto UPDATE | Cadastro > Produtos | `PATCH /api/produtos/{id}/` | UPDATE | valor_unitario=69.90 |

---

## 5. Cadastro — Pacientes

| Status | Teste | Menu | Endpoint | Acao | Dados |
|--------|-------|------|----------|------|-------|
| ✅ | Paciente INSERT #1 | Cadastro > Pacientes | `POST /api/pacientes/` | INSERT | Lucia Almeida, CPF=55566677788, Feminino, Ativo, psicologa=Fernanda |
| ✅ | Paciente INSERT #2 | Cadastro > Pacientes | `POST /api/pacientes/` | INSERT | Pedro Souza, 2015-09-20, Masculino, psicologo=Roberto |
| ✅ | Paciente INSERT #3 | Cadastro > Pacientes | `POST /api/pacientes/` | INSERT | Maria Clara Ferreira, 1975-12-01, psicologa=Camila |
| ✅ | Paciente UPDATE | Cadastro > Pacientes | `PATCH /api/pacientes/{id}/` | UPDATE | profissao="Professora", cidade="Rio de Janeiro" |
| ✅ | Paciente Detail | Cadastro > Pacientes > [nome] | `GET /api/pacientes/{id}/` | READ | Pagina de detalhe com abas |

---

## 6. Cadastro — Contatos e Servicos

| Status | Teste | Menu | Endpoint | Acao | Dados |
|--------|-------|------|----------|------|-------|
| ✅ | Contato Emerg INSERT | Cadastro > Contatos | `POST /api/contatos-emergencia/` | INSERT | Carlos Rocha, tel=21988001001, parentesco=Esposo, paciente=Lucia |
| ✅ | Contato Emerg UPDATE | Cadastro > Contatos | `PATCH /api/contatos-emergencia/{id}/` | UPDATE | telefone=21988009999 |
| ✅ | Paciente-Servico INSERT | Cadastro > Paciente Servico | `POST /api/paciente-servico/` | INSERT | paciente=Lucia, servico=primeiro tipo, inicio=29/06 |

---

## 7. Atendimento — Evolucao Clinica

| Status | Teste | Menu | Endpoint | Acao | Dados |
|--------|-------|------|----------|------|-------|
| ✅ | Evolucao INSERT | Atendimento > Evolucao | `POST /api/evolucao-clinica/` | INSERT | paciente=Lucia, psicologa=Fernanda, data=29/06, hora=09:00, texto="Melhora no sono" |
| ✅ | Evolucao UPDATE | Atendimento > Evolucao | `PATCH /api/evolucao-clinica/{id}/` | UPDATE | texto+= "Proximo: mindfulness" |

---

## 8. Atendimento — Avaliacao Neuropsicologica

| Status | Teste | Menu | Endpoint | Acao | Dados |
|--------|-------|------|----------|------|-------|
| ✅ | Avaliacao INSERT | Atendimento > Avaliacao | `POST /api/avaliacao-neuropsicologica/` | INSERT | paciente=Pedro, psicologo=Roberto, data=30/06, motivo="Dificuldade escolar", instrumentos="WISC-V", valor=1200 |

---

## 9. Atendimento — Reabilitacao

| Status | Teste | Menu | Endpoint | Acao | Dados |
|--------|-------|------|----------|------|-------|
| ✅ | Reabilitacao INSERT | Financeiro > Reabilitacao | `POST /api/reabilitacao-neuropsicologica/` | INSERT | paciente=Maria Clara, psicologa=Camila, inicio=29/06, 48 sessoes, 2x/semana, R$200/sessao |
| ✅ | Objetivo INSERT | Atendimento > Objetivos | `POST /api/reabilitacao-objetivo/` | INSERT | descricao="Fluencia verbal", status="Em Andamento" |
| ✅ | Objetivo UPDATE | Atendimento > Objetivos | `PATCH /api/reabilitacao-objetivo/{id}/` | UPDATE | comentario="Progresso de 40% apos 4 sessoes" |
| ✅ | Sessao Reab INSERT | Atendimento > Sessoes | `POST /api/reabilitacao-sessao/` | INSERT | data=01/07, hora=14:00, passos="Exercicios de nomeacao" |

---

## 10. Financeiro — Tabelas de Referencia

| Status | Teste | Menu | Endpoint | Acao | Dados |
|--------|-------|------|----------|------|-------|
| ✅ | Status Pagamento INSERT | Financeiro > Status Pgto | `POST /api/status-pagamento/` | INSERT | nome="Estornado" |
| ✅ | Tipo Transacao INSERT | Financeiro > Tipos Trans. | `POST /api/tipos-transacao/` | INSERT | nome="Supervisao" |
| ✅ | Status Objetivo INSERT | Financeiro > Status Obj. | `POST /api/status-objetivo-reabilitacao/` | INSERT | nome="Suspenso" |
| ✅ | Forma Cobranca INSERT | Financeiro > Formas Cobr. | `POST /api/formas-cobranca-reabilitacao/` | INSERT | nome="Valor Fixo Mensal" |

---

## 11. Financeiro — Transacoes

| Status | Teste | Menu | Endpoint | Acao | Dados |
|--------|-------|------|----------|------|-------|
| ✅ | Transacao INSERT | Financeiro > Transacoes | `POST /api/transacoes/` | INSERT | paciente=Lucia, psicologa=Fernanda, data=29/06, valor=250, status=Pago, desc="Sessao psicoterapia" |
| ✅ | Transacao UPDATE | Financeiro > Transacoes | `PATCH /api/transacoes/{id}/` | UPDATE | observacoes="Pago via PIX" |
| ✅ | Export CSV | Financeiro > Transacoes | `GET /api/transacoes/exportar/?formato=csv` | EXPORT | Retorna CSV com headers e dados |
| ✅ | Export XLSX | Financeiro > Transacoes | `GET /api/transacoes/exportar/?formato=xlsx` | EXPORT | Retorna XLSX com content-type correto |

---

## 12. Vendas

| Status | Teste | Menu | Endpoint | Acao | Dados |
|--------|-------|------|----------|------|-------|
| ✅ | Venda Vinculada INSERT | Vendas > Vinculadas | `POST /api/vendas-vinculadas/` | INSERT | paciente=Lucia, produto=Video, qtd=1, valor=69.90 → auto-cria transacao |
| ✅ | Venda Geral INSERT | Vendas > Gerais | `POST /api/vendas-geral/` | INSERT | comprador="Clinica Vida Nova", valor=350.00 |
| ✅ | Item Venda Geral INSERT | Vendas > Gerais | `POST /api/vendas-geral-itens/` | INSERT | produto=Video, qtd=5, valor_unit=69.90, total=349.50 |

---

## 13. Agenda — Calendario de Agendamentos

### Agendamentos da semana (29/06 - 04/07/2026)

| Status | Dia | Sala | Horario | Profissional | Paciente | Tipo | Duracao |
|--------|-----|------|---------|-------------|----------|------|---------|
| ✅ | Seg 29/06 | S1 | 08:00-09:00 | Dra. Fernanda | Lucia | Psicoterapia | 1h |
| ✅ | Seg 29/06 | S2 | 08:00-10:00 | Dr. Roberto | Pedro | Avaliacao | 2h |
| ✅ | Seg 29/06 | S3 | 09:00-11:00 | Dra. Camila | Maria Clara | Reabilitacao | 2h |
| ✅ | Ter 30/06 | S1 | 14:00-15:00 | Dra. Fernanda | Lucia | Psicoterapia | 1h |
| ✅ | Qua 01/07 | S2 | 10:00-13:00 | Dr. Roberto | Pedro | Avaliacao | 3h |
| ✅ | Qui 02/07 | S1 | 07:00-09:00 | Dra. Camila | Maria Clara | Reabilitacao | 2h |
| ✅ | Sex 03/07 | S3 | 16:00-18:00 | Dra. Fernanda | Maria Clara | Outro | 2h |
| ✅ | Sab 04/07 | S1 | 08:00-11:00 | Dr. Roberto | Lucia | Avaliacao | 3h |

### Validacoes de agendamento

| Status | Teste | Acao | Detalhe |
|--------|-------|------|---------|
| ✅ | Conflito mesma sala/hora | INSERT bloqueado | Sala 1, Seg 08:00 ja ocupada → HTTP 400 |
| ✅ | Horario antes 07:00 | INSERT bloqueado | hora_inicio=06:00 → "Horario minimo: 07:00" |
| ✅ | Horario apos 20:00 (seg-sex) | INSERT bloqueado | hora_fim=21:00 → "Horario maximo: 20:00" |
| ✅ | Horario apos 12:00 (sabado) | INSERT bloqueado | hora_fim=13:00 → "Horario maximo no sabado: 12:00" |
| ✅ | Domingo bloqueado | INSERT bloqueado | data=domingo → "Nao ha atendimento aos domingos" |
| ✅ | Salas diferentes mesmo horario | INSERT permitido | Sala 1 e Sala 2 ambas 08:00 → OK |

---

## 14. Controle de Acesso (Permissoes)

| Status | Teste | Usuario | Acao | Resultado esperado |
|--------|-------|---------|------|--------------------|
| ✅ | Admin acessa tudo | admin | GET todos endpoints | HTTP 200 |
| ✅ | Secretaria ve pacientes | secretaria | GET /api/pacientes/ | HTTP 200 |
| ✅ | Secretaria bloqueada evolucao | secretaria | GET /api/evolucao-clinica/ | HTTP 403 |
| ✅ | Secretaria bloqueada transacoes | secretaria | GET /api/transacoes/ | HTTP 403 |
| ✅ | Secretaria bloqueada avaliacao | secretaria | GET /api/avaliacao-*/ | HTTP 403 |
| ✅ | Secretaria read-only convenios | secretaria | POST /api/convenios/ | HTTP 403 |
| ✅ | Psicologa ve so seus dados | psicologa1 | GET /api/evolucao-clinica/ | So suas evolucoes |
| ✅ | Admin ve todos dados | admin | GET /api/evolucao-clinica/ | Todas evolucoes |

---

## Resumo

| Categoria | Total | Pass | Fail |
|-----------|-------|------|------|
| Autenticacao | 3 | 3 | 0 |
| Cadastro (lookups) | 8 | 8 | 0 |
| Profissionais | 5 | 5 | 0 |
| Produtos | 2 | 2 | 0 |
| Pacientes | 5 | 5 | 0 |
| Contatos/Servicos | 3 | 3 | 0 |
| Evolucao Clinica | 2 | 2 | 0 |
| Avaliacao | 1 | 1 | 0 |
| Reabilitacao | 4 | 4 | 0 |
| Financeiro (lookups) | 4 | 4 | 0 |
| Transacoes + Export | 4 | 4 | 0 |
| Vendas | 3 | 3 | 0 |
| Agendamentos | 14 | 14 | 0 |
| Permissoes | 8 | 8 | 0 |
| **TOTAL** | **66** | **66** | **0** |
