# Setup do Banco de Dados - NeuroCare

Este documento descreve como configurar o banco de dados PostgreSQL para o projeto NeuroCare em uma máquina local de usuário.

## 📋 Pré-requisitos

- **PostgreSQL 12+** instalado e rodando
- **Python 3.8+** instalado
- **pip** (gerenciador de pacotes Python)
- Clonar/copiar o repositório NeuroCare para o seu computador

## 🚀 Instalação Rápida

### Windows

1. Abra **Command Prompt** ou **PowerShell**
2. Navegue até a pasta do projeto:
   ```cmd
   cd C:\caminho\para\Neurocare
   ```

3. Execute o script de setup:
   ```cmd
   setup_postgres.bat
   ```

### Linux / macOS

1. Abra o **Terminal**
2. Navegue até a pasta do projeto:
   ```bash
   cd ~/caminho/para/Neurocare
   ```

3. Dê permissão de execução ao script:
   ```bash
   chmod +x setup_postgres.sh
   ```

4. Execute o script:
   ```bash
   ./setup_postgres.sh
   ```

## 📝 Configuração Manual

Se preferir fazer manualmente ou se os scripts tiverem problemas, siga estes passos:

### 1. Instalar dependências Python

```bash
pip install -r requirements.txt
```

### 2. Criar o banco de dados PostgreSQL

Abra o **psql** ou seu cliente PostgreSQL favorito e execute:

```bash
# Conectar ao PostgreSQL
psql -U postgres -h localhost

# Dentro do psql, criar o banco de dados
CREATE DATABASE neurocare;

# Listar bancos para confirmar
\l

# Conectar ao novo banco
\c neurocare
```

### 3. Configurar variáveis de ambiente

Edite o arquivo `.env` na raiz do projeto com suas credenciais PostgreSQL:

```env
NEUROCARE_DB_NAME=neurocare
NEUROCARE_DB_USER=postgres
NEUROCARE_DB_PASSWORD=sua_senha_aqui
NEUROCARE_DB_HOST=localhost
NEUROCARE_DB_PORT=5432
```

### 4. Executar as migrations do Django

```bash
python manage.py migrate
```

Isto criará todas as tabelas necessárias no schema `neurocare`.

### 5. Verificar o setup

```bash
python manage.py shell
```

Dentro do shell do Django:
```python
from django.db import connection
print(connection.introspection.table_names())
```

## 🔄 Resetar o banco de dados

Se você precisar descartar tudo e recomeçar:

### Opção 1: Via SQL diretamente

```bash
psql -U postgres -h localhost -c "DROP DATABASE neurocare;"
```

Depois execute novamente:
```bash
setup_postgres.bat   # Windows
./setup_postgres.sh  # Linux/macOS
```

### Opção 2: Via Django

```bash
python manage.py migrate --fake-initial zero  # Reverter todas as migrations
python manage.py migrate                      # Aplicar novamente
```

## 📊 Estrutura do Banco de Dados

O banco `neurocare` contém as seguintes tabelas principais:

- **pacientes**: Dados dos pacientes
- **profissionais**: Informações de profissionais de saúde
- **evolucao_clinica**: Registro de evolução clínica
- **avaliacao_neuropsicologica**: Avaliações neuropsicológicas
- **reabilitacao_sessao**: Sessões de reabilitação
- **transacoes**: Registros de transações financeiras
- **vendas**: Dados de vendas e serviços

(e outras tabelas de configuração e suporte)

## 🐛 Solução de Problemas

### Erro: "psycopg2: can't adapt type datetime.date"

```bash
pip install --upgrade psycopg2-binary
```

### Erro: "permission denied for schema neurocare"

Verifique se o usuário PostgreSQL tem as permissões corretas:

```sql
GRANT ALL PRIVILEGES ON SCHEMA neurocare TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA neurocare TO postgres;
```

### Erro: "database already exists"

Limpe o banco primeiro:
```bash
psql -U postgres -h localhost -c "DROP DATABASE IF EXISTS neurocare;"
```

### PostgreSQL não está rodando

- **Windows**: Procure por "Services" e inicie o serviço PostgreSQL
- **macOS**: `brew services start postgresql` (se instalado via Homebrew)
- **Linux**: `sudo systemctl start postgresql`

## 🔗 Conexão com o banco para testes

Para conectar ao banco e executar queries:

```bash
psql -U postgres -h localhost -d neurocare
```

Alguns comandos úteis do psql:
```sql
\dt                    -- Listar tabelas
\d nome_tabela         -- Descrever estrutura de uma tabela
\dn                    -- Listar schemas
SELECT * FROM pg_tables WHERE schemaname = 'neurocare';  -- Listar tabelas do schema
```

## 📞 Suporte

Se você enfrentar problemas:

1. Verifique se PostgreSQL está rodando
2. Confirme as credenciais no arquivo `.env`
3. Teste a conexão: `psql -U postgres -h localhost`
4. Verifique o output do script para mensagens de erro
5. Consulte a documentação do Django: https://docs.djangoproject.com/en/5.2/

---

**Última atualização**: 2025-01-15
