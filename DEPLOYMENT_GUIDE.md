# Guia de Deployment - NeuroCare

Este documento descreve como mover o código do NeuroCare para uma nova máquina (máquina do usuário para testes).

## 📋 Cenários de Deployment

### Cenário 1: Git Clone (Recomendado se o repo estiver no GitHub)
Se o código estiver num repositório Git remoto (GitHub, GitLab, etc).

### Cenário 2: ZIP/Arquivo Compactado
Se você tiver o código em um arquivo .zip ou similar.

### Cenário 3: Cópia Manual
Se você quiser copiar diretamente entre pastas.

---

## 🎯 Cenário 1: Git Clone (Recomendado)

Esta é a melhor prática se o código estiver num repositório Git remoto.

### Pré-requisitos
- Git instalado (https://git-scm.com/download)
- Acesso ao repositório remoto (GitHub, GitLab, etc.)
- SSH keys ou credentials configuradas (opcional, para repos privados)

### Passos

#### 1. Clonar o repositório

```bash
# Navegar para o local onde quer instalar o projeto
cd C:\Users\SeuUsuario\Documents
# ou no Linux/Mac
cd ~/Documents

# Clonar o repositório
git clone https://github.com/seu-usuario/neurocare.git
# ou com SSH (se tiver chaves configuradas)
git clone git@github.com:seu-usuario/neurocare.git

# Entrar no diretório do projeto
cd neurocare
```

#### 2. Instalar dependências Python

```bash
# Criar um ambiente virtual (opcional, mas recomendado)
python -m venv venv

# Ativar o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Instalar as dependências
pip install -r requirements.txt
```

#### 3. Configurar arquivo .env

```bash
# Copiar o arquivo de exemplo
cp .env.example .env
# ou no Windows
copy .env.example .env

# Editar o arquivo .env com suas credenciais PostgreSQL locais
# Usar seu editor favorito (VS Code, Sublime, Notepad++, etc)
```

Conteúdo esperado do `.env`:
```env
NEUROCARE_SECRET_KEY=sua_chave_aqui
NEUROCARE_DEBUG=true
NEUROCARE_ALLOWED_HOSTS=127.0.0.1,localhost

NEUROCARE_DB_NAME=neurocare
NEUROCARE_DB_USER=postgres
NEUROCARE_DB_PASSWORD=sua_senha_postgres
NEUROCARE_DB_HOST=localhost
NEUROCARE_DB_PORT=5432
```

#### 4. Setup do banco de dados

```bash
# Windows
setup_postgres.bat

# Linux/macOS
chmod +x setup_postgres.sh
./setup_postgres.sh
```

#### 5. Verificar a instalação

```bash
# Rodar o servidor de desenvolvimento
python manage.py runserver
```

Abra no navegador: http://localhost:8000

---

## 📦 Cenário 2: Via Arquivo Compactado (ZIP)

Se você recebeu o código como arquivo .zip.

### Passos

#### 1. Extrair o arquivo

**Windows:**
- Clique com botão direito no arquivo .zip
- Selecione "Extrair tudo..."
- Escolha o local de destino

**Linux/macOS:**
```bash
unzip neurocare.zip
cd neurocare
```

#### 2-5. Repetir os passos 2-5 do Cenário 1

---

## 💾 Cenário 3: Cópia Manual entre Pastas

Se você quer copiar de uma máquina para outra manualmente.

### Passos

#### 1. Copiar o diretório do projeto

**Windows (PowerShell):**
```powershell
Copy-Item -Path "C:\Users\origem\OneDrive\Neurocare" `
          -Destination "C:\Users\destino\Documents\neurocare" `
          -Recurse
```

**Linux/macOS:**
```bash
cp -r ~/OneDrive/Neurocare ~/Documents/neurocare
```

#### 2. Entrar no diretório

```bash
cd ~/Documents/neurocare
# ou
cd C:\Users\destino\Documents\neurocare
```

#### 3-5. Repetir os passos 2-5 do Cenário 1

---

## 📋 Checklist Pós-Instalação

Após mover o código, verifique:

- [ ] Python está instalado (`python --version`)
- [ ] PostgreSQL está rodando e acessível
- [ ] Arquivo `.env` foi criado com credenciais corretas
- [ ] Dependências foram instaladas (`pip list | grep django`)
- [ ] Database foi criado e migrations rodaram (`psql -d neurocare -c "\dt"`)
- [ ] Servidor inicia sem erros (`python manage.py runserver`)
- [ ] URL http://localhost:8000 responde corretamente

---

## 🚀 Estrutura de Diretórios Esperada

Após a instalação, você deve ter:

```
neurocare/
├── .env                          # Arquivo de configuração (criar/editar)
├── .env.example                  # Exemplo de .env
├── manage.py                     # Script principal Django
├── requirements.txt              # Dependências Python
├── setup_postgres.py             # Script de setup do banco
├── setup_postgres.bat
├── setup_postgres.sh
├── DATABASE_SETUP.md             # Este documento
├── neurocare_project/            # Configurações do projeto
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── pacientes/                    # Apps Django
├── profissionais/
├── evolucao_clinica/
├── reabilitacao_sessao/
├── vendas/
├── templates/                    # Templates HTML
├── static/                       # Arquivos estáticos
├── migrations/                   # Migrations do banco
└── ...
```

---

## 🔄 Atualizar Código Posteriormente (Git)

Se usar Git, para atualizar para a versão mais recente:

```bash
# Entrar no diretório do projeto
cd neurocare

# Buscar as mudanças mais recentes
git fetch origin

# Aplicar as mudanças na branch atual
git pull origin main
# ou, dependendo do nome da branch
git pull origin master

# Instalar qualquer dependência nova
pip install -r requirements.txt

# Rodar migrations se houver novas
python manage.py migrate
```

---

## 🐛 Solução de Problemas Comuns

### Erro: "No module named 'django'"

```bash
# Ativar o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Reinstalar dependências
pip install -r requirements.txt
```

### Erro: "database 'neurocare' does not exist"

```bash
# Rodar o setup do banco novamente
python setup_postgres.py
# ou
setup_postgres.bat
```

### Erro: "connection refused" PostgreSQL

```bash
# Verificar se PostgreSQL está rodando
# Windows: procure "Services" e inicie PostgreSQL
# Linux: sudo systemctl start postgresql
# macOS: brew services start postgresql
```

### Erro: "permission denied" ao executar scripts

**Linux/macOS:**
```bash
chmod +x setup_postgres.sh
chmod +x *.sh
```

### Porta 8000 já está em uso

```bash
# Use uma porta diferente
python manage.py runserver 8001
```

---

## 📊 Resumo dos Comandos Essenciais

| Tarefa | Windows | Linux/macOS |
|--------|---------|------------|
| Clonar repo | `git clone ...` | `git clone ...` |
| Criar venv | `python -m venv venv` | `python3 -m venv venv` |
| Ativar venv | `venv\Scripts\activate` | `source venv/bin/activate` |
| Instalar deps | `pip install -r requirements.txt` | `pip install -r requirements.txt` |
| Setup banco | `setup_postgres.bat` | `./setup_postgres.sh` |
| Rodar servidor | `python manage.py runserver` | `python manage.py runserver` |
| Rodar migrations | `python manage.py migrate` | `python manage.py migrate` |
| Ver banco | `psql -d neurocare` | `psql -d neurocare` |

---

## 💡 Dicas Importantes

1. **Use ambientes virtuais Python** - Evita conflitos de versões de pacotes
2. **Nunca commit do .env com credenciais reais** - Sempre use .env.example
3. **Mantenha o .env fora do Git** - Deve estar em .gitignore
4. **Use Git para colaboração** - Facilita sync de código entre desenvolvedores
5. **Documente mudanças no DB** - Sempre crie migrations para alterações de schema

---

## 📞 Próximos Passos

Após instalar e rodar localmente:

1. Explorar a estrutura do projeto
2. Ler a documentação das apps
3. Começar os testes conforme planejado
4. Reportar bugs ou problemas encontrados
5. Criar branches para novas funcionalidades

---

**Última atualização**: 2025-01-15
