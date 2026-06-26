# Research — Gaps NeuroCare v1

## R1: Controle de acesso DRF
- **Decisao**: Custom DRF permissions com perfil baseado em PerfilAcesso
- **Racional**: DRF permite `BasePermission` customizado que checa o perfil do usuario via FK `tb_usuario.id_perfil_acesso`
- **Alternativas**: Django Groups (mais complexo para o caso), django-guardian (overkill para object-level simples)
- **Abordagem**: 3 permission classes — `IsSecretaria`, `IsPsicologa`, `IsAdmin`. ViewSets aplicam `get_permissions()` com base na action (list/create/update/delete)

## R2: Exportacao CSV/Excel
- **Decisao**: Endpoint DRF customizado que retorna CSV via `HttpResponse` com `text/csv`
- **Racional**: Nao precisa de lib extra para CSV. Para Excel, usar `openpyxl` (leve, ja padrao)
- **Alternativas**: django-import-export (pesado demais), pandas (desnecessario)

## R3: Filtragem por psicologo
- **Decisao**: Override `get_queryset()` nos ViewSets para filtrar por `id_psicologo_responsavel` do usuario logado
- **Racional**: Simples, nao requer lib extra. O mapeamento usuario Django -> tb_usuario eh feito via email ou campo custom
- **Abordagem**: Criar middleware ou mixin que injeta o filtro automaticamente

## R4: Upload de PDF
- **Decisao**: Django FileField com storage local ou S3
- **Racional**: Simples para MVP. Pode migrar para S3 depois
- **Alternativas**: Armazenar no Postgres (BYTEA) — nao recomendado para PDFs grandes

## R5: Auto-criacao de transacao
- **Decisao**: Signal `post_save` no model VendaVinculada/VendaGeral
- **Racional**: Desacoplado do view, garante consistencia
- **Alternativas**: Override no serializer.create() — mais acoplado mas mais previsivel
- **Escolha final**: Override no serializer.create() para maior controle

## R6: Perfil integrado do paciente
- **Decisao**: Frontend — pagina de detalhe do paciente com tabs (Dados, Evolucao, Avaliacao, Reabilitacao, Vendas)
- **Racional**: Melhor UX que navegar entre modulos separados

## R7: Filtros na UI
- **Decisao**: Componente FilterBar reutilizavel com date range, selects, e search
- **Racional**: Todos os endpoints ja suportam filtros via query params
