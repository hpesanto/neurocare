"""
NeuroCare E2E Test Suite
========================
Executa testes de INSERT + UPDATE em todos os modulos da aplicacao.
Requer: pip install requests
Uso:    docker compose down -v && docker compose up --build -d
        (aguardar ~15s)
        python tests/test_e2e.py

Resultado esperado: 66 PASS / 0 FAIL
"""

import sys
import requests

BASE = "http://localhost:8000/api"
S = requests.Session()

PASS = FAIL = 0
IDS = {}


def auth(username, password):
    r = S.post(f"{BASE}/token/", json={"username": username, "password": password})
    if r.status_code != 200:
        print(f"FATAL: Login failed for {username}: {r.text}")
        sys.exit(1)
    S.headers["Authorization"] = f"Bearer {r.json()['access']}"


def test(desc, method, url, data=None, expect=None):
    global PASS, FAIL
    fn = getattr(S, method)
    r = fn(f"{BASE}/{url}", json=data) if data else fn(f"{BASE}/{url}")
    ok = r.status_code in (200, 201, 204) if not expect else r.status_code == expect
    if ok:
        PASS += 1
        d = r.json() if r.content and r.headers.get("content-type", "").startswith("application/json") else {}
        id_val = d.get("id", "")
        print(f"  PASS {desc} (HTTP {r.status_code}){f' id={str(id_val)[:8]}' if id_val else ''}")
        return d
    else:
        FAIL += 1
        print(f"  FAIL {desc} (HTTP {r.status_code}): {r.text[:200]}")
        return {}


def test_status(desc, method, url, data=None, expect=200):
    global PASS, FAIL
    fn = getattr(S, method)
    r = fn(f"{BASE}/{url}", json=data) if data else fn(f"{BASE}/{url}")
    if r.status_code == expect:
        PASS += 1
        print(f"  PASS {desc} (HTTP {r.status_code})")
    else:
        FAIL += 1
        print(f"  FAIL {desc} (HTTP {r.status_code}, expected {expect}): {r.text[:150]}")


def get_id(ep, name_field="nome", name_contains=None, index=0):
    r = S.get(f"{BASE}/{ep}/?page_size=100")
    results = r.json().get("results", [])
    if name_contains:
        results = [x for x in results if name_contains in str(x.get(name_field, ""))]
    return results[index]["id"] if results else None


# ==============================================================
print("=" * 60)
print(" PLANO DE TESTES E2E - NeuroCare")
print("=" * 60)

auth("admin", "admin123")

# --- 1-2: PERFIL + PROFISSIONAIS ---
print("\n--- 1. Perfil de Acesso: INSERT + UPDATE ---")
d = test("INSERT Perfil", "post", "perfis-acesso/", {"nome": "TestPerfil", "descricao": "Teste"})
IDS["perfil"] = d.get("id")
test("UPDATE Perfil", "patch", f"perfis-acesso/{IDS['perfil']}/", {"descricao": "Teste atualizado"})

print("\n--- 2. Profissionais: INSERT x3 + UPDATE ---")
pa_psi = get_id("perfis-acesso", name_contains="Psicologo")
for name, login, email in [
    ("Dra. Fernanda Costa", "t_fernanda", "t_fernanda@nc.com"),
    ("Dr. Roberto Lima", "t_roberto", "t_roberto@nc.com"),
    ("Dra. Camila Santos", "t_camila", "t_camila@nc.com"),
]:
    d = test(f"INSERT {name}", "post", "profissionais/", {
        "nome": name, "email": email, "login": login,
        "senha": "Test@2026", "id_perfil_acesso": pa_psi,
    })
    IDS[f"prof_{login}"] = d.get("id")
test("UPDATE Fernanda", "patch", f"profissionais/{IDS['prof_t_fernanda']}/", {"nome": "Dra. Fernanda Costa Silva"})

# --- 3-12: LOOKUP TABLES ---
print("\n--- 3. Convenio: INSERT + UPDATE ---")
d = test("INSERT Convenio", "post", "convenios/", {"nome": "TestConvenio"})
IDS["conv"] = d.get("id")
test("UPDATE Convenio", "patch", f"convenios/{IDS['conv']}/", {"nome": "TestConvenio Premium"})

print("\n--- 4. Forma Pagamento: INSERT ---")
test("INSERT FormaPgto", "post", "formas-pagamento/", {"nome": "TestFormaPgto"})

print("\n--- 5. Tipo Produto: INSERT ---")
test("INSERT TipoProd", "post", "tipos-produto/", {"nome": "TestTipoProd"})

print("\n--- 6. Produto: INSERT + UPDATE ---")
tp = get_id("tipos-produto", name_contains="TestTipoProd")
d = test("INSERT Produto", "post", "produtos/", {"nome": "TestProduto", "valor_unitario": "79.90", "id_tipo_produto": tp})
IDS["prod"] = d.get("id")
test("UPDATE Produto", "patch", f"produtos/{IDS['prod']}/", {"valor_unitario": "69.90"})

print("\n--- 7. Faixa Etaria: INSERT ---")
test("INSERT FaixaEtaria", "post", "faixas-etarias/", {"nome": "TestFaixa", "descricao": "Teste"})

print("\n--- 8. Tipo Servico: INSERT ---")
test("INSERT TipoServico", "post", "tipos-servico/", {"nome": "TestTipoServico"})

print("\n--- 9. Status Pagamento: INSERT ---")
test("INSERT StatusPgto", "post", "status-pagamento/", {"nome": "TestStatusPgto"})

print("\n--- 10. Tipo Transacao: INSERT ---")
test("INSERT TipoTransacao", "post", "tipos-transacao/", {"nome": "TestTipoTrans"})

print("\n--- 11. Status Objetivo: INSERT ---")
test("INSERT StatusObj", "post", "status-objetivo-reabilitacao/", {"nome": "TestStatusObj"})

print("\n--- 12. Forma Cobranca: INSERT ---")
test("INSERT FormaCobranca", "post", "formas-cobranca-reabilitacao/", {"nome": "TestFormaCobranca"})

# --- 13-15: PACIENTES + CONTATOS + SERVICOS ---
fe = get_id("faixas-etarias")
conv = get_id("convenios")
fp = get_id("formas-pagamento")
sp = get_id("status-pagamento", name_contains="Pago")
tt = get_id("tipos-transacao")
ts = get_id("tipos-servico")
fcr = get_id("formas-cobranca-reabilitacao")
sor = get_id("status-objetivo-reabilitacao", name_contains="Andamento")

print("\n--- 13. Pacientes: INSERT x3 + UPDATE ---")
d = test("INSERT Pac1", "post", "pacientes/", {"nome_completo": "TestPac Lucia", "data_nascimento": "1988-03-15", "cpf": "99988877766", "genero": "Feminino", "telefone_principal": "21900000001", "status_paciente": "Ativo", "id_psicologo_responsavel": IDS["prof_t_fernanda"], "id_convenio": conv, "id_faixa_etaria": fe})
IDS["pac1"] = d.get("id")
d = test("INSERT Pac2", "post", "pacientes/", {"nome_completo": "TestPac Pedro", "data_nascimento": "2015-09-20", "telefone_principal": "21900000002", "genero": "Masculino", "status_paciente": "Ativo", "id_psicologo_responsavel": IDS["prof_t_roberto"]})
IDS["pac2"] = d.get("id")
d = test("INSERT Pac3", "post", "pacientes/", {"nome_completo": "TestPac Maria", "data_nascimento": "1975-12-01", "telefone_principal": "21900000003", "status_paciente": "Ativo", "id_psicologo_responsavel": IDS["prof_t_camila"]})
IDS["pac3"] = d.get("id")
test("UPDATE Pac1", "patch", f"pacientes/{IDS['pac1']}/", {"profissao": "Professora", "endereco_cidade": "Rio de Janeiro"})

print("\n--- 14. Contato Emergencia: INSERT + UPDATE ---")
d = test("INSERT Contato", "post", "contatos-emergencia/", {"id_paciente": IDS["pac1"], "nome_contato": "TestContato", "telefone_contato": "21900009999", "parentesco": "Esposo"})
IDS["ce"] = d.get("id")
test("UPDATE Contato", "patch", f"contatos-emergencia/{IDS['ce']}/", {"telefone_contato": "21900008888"})

print("\n--- 15. Paciente-Servico: INSERT ---")
test("INSERT PacServico", "post", "paciente-servico/", {"id_paciente": IDS["pac1"], "id_tipo_servico": ts, "data_inicio": "2026-06-29"})

# --- 16-20: ATENDIMENTO ---
print("\n--- 16. Evolucao Clinica: INSERT + UPDATE ---")
d = test("INSERT Evolucao", "post", "evolucao-clinica/", {"id_paciente": IDS["pac1"], "id_psicologo": IDS["prof_t_fernanda"], "data_sessao": "2026-06-29", "hora_sessao": "09:00", "evolucao_texto": "Teste evolucao"})
IDS["ec"] = d.get("id")
test("UPDATE Evolucao", "patch", f"evolucao-clinica/{IDS['ec']}/", {"evolucao_texto": "Teste evolucao atualizado"})

print("\n--- 17. Avaliacao Neuropsicologica: INSERT ---")
d = test("INSERT Avaliacao", "post", "avaliacao-neuropsicologica/", {"id_paciente": IDS["pac2"], "id_psicologo": IDS["prof_t_roberto"], "data_avaliacao": "2026-06-30", "motivo_avaliacao": "Teste motivo", "valor_avaliacao": "1200.00"})
IDS["av"] = d.get("id")

print("\n--- 18. Reabilitacao Neuropsicologica: INSERT ---")
d = test("INSERT Reabilitacao", "post", "reabilitacao-neuropsicologica/", {"id_paciente": IDS["pac3"], "id_psicologo": IDS["prof_t_camila"], "data_inicio": "2026-06-29", "programa_descricao": "Teste programa", "num_sessoes_planejadas": 24, "frequencia": "2x semana", "id_forma_cobranca": fcr, "valor_por_sessao": "200.00"})
IDS["rn"] = d.get("id")

print("\n--- 19. Objetivo Reabilitacao: INSERT + UPDATE ---")
d = test("INSERT Objetivo", "post", "reabilitacao-objetivo/", {"id_reabilitacao": IDS["rn"], "descricao": "Teste objetivo", "id_status_objetivo": sor})
IDS["ro"] = d.get("id")
test("UPDATE Objetivo", "patch", f"reabilitacao-objetivo/{IDS['ro']}/", {"comentario_status": "Progresso 40%"})

print("\n--- 20. Sessao Reabilitacao: INSERT ---")
test("INSERT SessaoReab", "post", "reabilitacao-sessao/", {"id_reabilitacao": IDS["rn"], "data_sessao": "2026-07-01", "hora_sessao": "14:00", "passos_realizados": "Teste passos"})

# --- 21-24: FINANCEIRO + VENDAS ---
print("\n--- 21. Venda Vinculada: INSERT (auto-transacao) ---")
test("INSERT VendaVinc", "post", "vendas-vinculadas/", {"id_paciente": IDS["pac1"], "id_produto": IDS["prod"], "data_venda": "2026-06-29", "quantidade": 1, "valor_unitario": "69.90", "valor_total_produto": "69.90", "id_forma_pagamento": fp})

print("\n--- 22. Venda Geral: INSERT ---")
d = test("INSERT VendaGeral", "post", "vendas-geral/", {"data_venda": "2026-06-30", "nome_comprador": "TestComprador", "valor_total_transacao": "350.00", "id_forma_pagamento": fp})
IDS["vg"] = d.get("id")

print("\n--- 23. Item Venda Geral: INSERT ---")
test("INSERT VendaGeralItem", "post", "vendas-geral-itens/", {"id_venda_geral": IDS["vg"], "id_produto": IDS["prod"], "quantidade": 5, "valor_unitario": "69.90", "valor_total_item": "349.50"})

print("\n--- 24. Transacao Financeira: INSERT + UPDATE ---")
d = test("INSERT Transacao", "post", "transacoes/", {"id_paciente": IDS["pac1"], "id_psicologo": IDS["prof_t_fernanda"], "id_tipo_transacao": tt, "data_transacao": "2026-06-29", "valor": "250.00", "id_forma_pagamento": fp, "id_status_pagamento": sp, "descricao": "Teste sessao"})
IDS["tf"] = d.get("id")
test("UPDATE Transacao", "patch", f"transacoes/{IDS['tf']}/", {"observacoes": "Pago via PIX"})

# --- 25: EXPORTACAO ---
print("\n--- 25. Exportacao: CSV + XLSX ---")
r = S.get(f"{BASE}/transacoes/exportar/?formato=csv")
if r.status_code == 200 and "Data" in r.text:
    PASS += 1; print(f"  PASS Export CSV (HTTP 200, {len(r.text)} bytes)")
else:
    FAIL += 1; print(f"  FAIL Export CSV (HTTP {r.status_code})")

r = S.get(f"{BASE}/transacoes/exportar/?formato=xlsx")
if r.status_code == 200 and "spreadsheet" in r.headers.get("content-type", ""):
    PASS += 1; print(f"  PASS Export XLSX (HTTP 200)")
else:
    FAIL += 1; print(f"  FAIL Export XLSX (HTTP {r.status_code})")

# --- 26: AGENDAMENTOS ---
print("\n--- 26. Agendamentos: 8 na semana 29/06 - 04/07 ---")
agendamentos = [
    {"prof": "prof_t_fernanda", "pac": "pac1", "sala": 1, "data": "2026-06-29", "hi": "08:00", "hf": "09:00", "tipo": "Psicoterapia", "desc": "Seg S1 08-09 (1h)"},
    {"prof": "prof_t_roberto",  "pac": "pac2", "sala": 2, "data": "2026-06-29", "hi": "08:00", "hf": "10:00", "tipo": "Avaliacao",    "desc": "Seg S2 08-10 (2h)"},
    {"prof": "prof_t_camila",   "pac": "pac3", "sala": 3, "data": "2026-06-29", "hi": "09:00", "hf": "11:00", "tipo": "Reabilitacao", "desc": "Seg S3 09-11 (2h)"},
    {"prof": "prof_t_fernanda", "pac": "pac1", "sala": 1, "data": "2026-06-30", "hi": "14:00", "hf": "15:00", "tipo": "Psicoterapia", "desc": "Ter S1 14-15 (1h)"},
    {"prof": "prof_t_roberto",  "pac": "pac2", "sala": 2, "data": "2026-07-01", "hi": "10:00", "hf": "13:00", "tipo": "Avaliacao",    "desc": "Qua S2 10-13 (3h)"},
    {"prof": "prof_t_camila",   "pac": "pac3", "sala": 1, "data": "2026-07-02", "hi": "07:00", "hf": "09:00", "tipo": "Reabilitacao", "desc": "Qui S1 07-09 (2h)"},
    {"prof": "prof_t_fernanda", "pac": "pac3", "sala": 3, "data": "2026-07-03", "hi": "16:00", "hf": "18:00", "tipo": "Outro",        "desc": "Sex S3 16-18 (2h)"},
    {"prof": "prof_t_roberto",  "pac": "pac1", "sala": 1, "data": "2026-07-04", "hi": "08:00", "hf": "11:00", "tipo": "Avaliacao",    "desc": "Sab S1 08-11 (3h)"},
]
for ag in agendamentos:
    test(f"INSERT {ag['desc']}", "post", "agendamentos/", {
        "id_profissional": IDS[ag["prof"]], "id_paciente": IDS[ag["pac"]],
        "sala": ag["sala"], "data": ag["data"],
        "hora_inicio": ag["hi"], "hora_fim": ag["hf"], "tipo": ag["tipo"],
    })

# --- 27: VALIDACOES AGENDAMENTO ---
print("\n--- 27. Validacoes de agendamento ---")
test_status("Conflito sala/hora", "post", "agendamentos/", {"id_profissional": IDS["prof_t_fernanda"], "id_paciente": IDS["pac1"], "sala": 1, "data": "2026-06-29", "hora_inicio": "08:00", "hora_fim": "09:00", "tipo": "Outro"}, expect=400)
test_status("Antes 07:00", "post", "agendamentos/", {"id_profissional": IDS["prof_t_fernanda"], "id_paciente": IDS["pac1"], "sala": 1, "data": "2026-07-03", "hora_inicio": "06:00", "hora_fim": "07:00", "tipo": "Outro"}, expect=400)
test_status("Apos 20:00 seg-sex", "post", "agendamentos/", {"id_profissional": IDS["prof_t_fernanda"], "id_paciente": IDS["pac1"], "sala": 1, "data": "2026-07-03", "hora_inicio": "19:00", "hora_fim": "21:00", "tipo": "Outro"}, expect=400)
test_status("Sab apos 12:00", "post", "agendamentos/", {"id_profissional": IDS["prof_t_fernanda"], "id_paciente": IDS["pac1"], "sala": 1, "data": "2026-07-04", "hora_inicio": "11:00", "hora_fim": "13:00", "tipo": "Outro"}, expect=400)
test_status("Domingo bloqueado", "post", "agendamentos/", {"id_profissional": IDS["prof_t_fernanda"], "id_paciente": IDS["pac1"], "sala": 1, "data": "2026-07-05", "hora_inicio": "09:00", "hora_fim": "10:00", "tipo": "Outro"}, expect=400)

# --- 28: PERMISSOES ---
print("\n--- 28. Permissoes por perfil ---")
test("GET auth/me (admin)", "get", "auth/me/")

# Secretaria
auth("secretaria", "test123")
test_status("Secretaria GET pacientes", "get", "pacientes/", expect=200)
test_status("Secretaria GET evolucao BLOQUEADA", "get", "evolucao-clinica/", expect=403)
test_status("Secretaria GET transacoes BLOQUEADA", "get", "transacoes/", expect=403)

# Restore admin
auth("admin", "admin123")

# ==============================================================
print("\n" + "=" * 60)
print(f" RESULTADO: {PASS} PASS / {FAIL} FAIL / {PASS + FAIL} TOTAL")
print("=" * 60)
sys.exit(1 if FAIL else 0)
