# Plano de Implementacao — Gaps NeuroCare v1

## Contexto
Aplicacao validada contra Espec_NeuroCare_2025.docx.
39 requisitos implementados, 6 parciais, 7 pendentes.
Este plano endereca os 7 gaps por ordem de prioridade.

## Fases de implementacao

### Fase 1: Controle de Acesso (P1 + P3) — Backend
**Arquivos**: `backend/neurocare_project/permissions.py` (novo), todos os `viewsets.py`

1. Criar `permissions.py` com 3 classes:
   - `IsAdmin` — checa se tb_usuario.id_perfil_acesso.nome == "Administrador"
   - `IsPsicologaOrAdmin` — Psicologo ou Admin
   - `IsSecretariaOrAbove` — qualquer perfil autenticado
2. Criar mixin `OwnPatientsQuerysetMixin` que filtra queryset por psicologo logado
3. Aplicar permissions nos ViewSets:
   - Evolucao, Avaliacao, Reabilitacao: `IsPsicologaOrAdmin` + filtro por psicologo
   - Transacoes: `IsPsicologaOrAdmin` + filtro
   - Cadastro pacientes: todos autenticados, mas Psicologa so ve os seus
4. Mapear `auth_user` -> `tb_usuario` via email match
5. Endpoint `/api/auth/me/` retornar tambem o perfil

### Fase 2: Exportacao Financeira (P2) — Backend + Frontend
**Arquivos**: `backend/transacoes/views.py` (novo), `frontend/src/pages/financeiro/TransacoesPage.tsx`

1. Criar view `exportar_transacoes` que aceita query params de filtro
2. Gerar CSV com `csv.writer` ou XLSX com `openpyxl`
3. Colunas: Data, Paciente, CPF Pagador, Endereco, Email, Tipo, Descricao, Valor, Forma Pgto, Status
4. Botao "Exportar" no frontend com selects de formato e filtros de data

### Fase 3: Upload de Laudo PDF (P4) — Backend + Frontend
**Arquivos**: `backend/avaliacao_neuropsicologica/viewsets.py`, `backend/neurocare_project/settings.py`, `frontend/src/pages/atendimento/AvaliacaoPage.tsx`

1. Configurar `MEDIA_ROOT` e `MEDIA_URL` no settings
2. Adicionar `parser_classes` com `MultiPartParser` no ViewSet
3. Tratar upload no serializer
4. Botao de upload no formulario de avaliacao

### Fase 4: Vinculacao Automatica Vendas -> Transacoes (P5) — Backend
**Arquivos**: `backend/vendas/serializers.py`, `backend/vendas_geral/serializers.py`

1. Override `create()` nos serializers de VendaVinculada e VendaGeral
2. Criar TransacaoFinanceira automaticamente com os dados da venda
3. Vincular via FK `id_venda_vinculada_paciente` ou `id_venda_geral`

### Fase 5: Perfil do Paciente com Abas (P6) — Frontend
**Arquivos**: `frontend/src/pages/cadastro/PacienteDetailPage.tsx` (novo), `frontend/src/App.tsx`

1. Criar pagina de detalhe do paciente com tabs Bootstrap
2. Tabs: Dados | Evolucao | Avaliacao | Reabilitacao | Vendas
3. Cada tab carrega os dados filtrados por `id_paciente`
4. Rota: `/cadastro/pacientes/:id`

### Fase 6: Filtros Avancados na UI (P7) — Frontend
**Arquivos**: `frontend/src/components/FilterBar.tsx` (novo), paginas de listagem

1. Componente FilterBar reutilizavel com:
   - DateRange (data inicio / data fim)
   - FkSelect para psicologo, tipo, status
   - Botao aplicar/limpar
2. Integrar com `useCrud` hook passando query params
3. Aplicar em: Transacoes, Evolucao, Avaliacao, Vendas

## Estimativa de esforco
| Fase | Complexidade | Arquivos |
|------|-------------|----------|
| 1. Permissoes | Alta | ~15 arquivos |
| 2. Exportacao | Media | 3 arquivos |
| 3. Upload PDF | Baixa | 3 arquivos |
| 4. Auto-transacao | Baixa | 2 arquivos |
| 5. Perfil paciente | Media | 3 arquivos |
| 6. Filtros UI | Media | 5+ arquivos |

## Ordem recomendada
Fase 1 -> Fase 2 -> Fase 4 -> Fase 3 -> Fase 5 -> Fase 6
(Permissoes primeiro pois impacta todos os endpoints)
