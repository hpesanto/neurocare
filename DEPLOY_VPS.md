# Deploy NeuroCare em VPS

Guia completo para deploy da aplicacao NeuroCare em uma VPS (Ubuntu 22.04/24.04).

---

## 1. Requisitos da VPS

| Item | Minimo |
|------|--------|
| SO | Ubuntu 22.04 ou 24.04 LTS |
| RAM | 2 GB |
| Disco | 20 GB |
| CPU | 1 vCPU |
| Portas | 22 (SSH), 80 (HTTP), 443 (HTTPS) |

---

## 2. Acesso inicial a VPS

```bash
ssh root@SEU_IP_DA_VPS
```

### 2.1 Atualizar o sistema

```bash
apt update && apt upgrade -y
```

### 2.2 Criar usuario de deploy (nao usar root)

```bash
adduser neurocare
usermod -aG sudo neurocare
su - neurocare (psico10!)
```

---

## 3. Instalar Docker e Docker Compose

```bash
# Dependencias
sudo apt install -y ca-certificates curl gnupg lsb-release

# Chave GPG do Docker
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Repositorio Docker
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

#### atenção com observação para versões de inux ####
# Em vez de $(lsb_release -cs), use "noble" fixo
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu noble stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
################################################################


# Instalar Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Adicionar usuario ao grupo docker (evita usar sudo)
sudo usermod -aG docker neurocare
newgrp docker

# Verificar instalacao
docker --version --* Docker version 29.6.1, build 8900f1d
docker compose version --*** Docker Compose version v5.2.0
```

---

## 4. Clonar o repositorio

```bash
cd /home/neurocare
git clone https://github.com/hpesanto/neurocare.git
cd neurocare
```

---

## 5. Configurar variaveis de ambiente

### 5.1 Criar arquivo .env

```bash
cp .env.example .env
nano .env
```

### 5.2 Conteudo do .env (EDITE os valores)

```env
# SEGURANCA: gere uma chave unica com o comando abaixo
# python3 -c "import secrets; print(secrets.token_urlsafe(50))"
NEUROCARE_SECRET_KEY=COLE_SUA_CHAVE_SECRETA_AQUI

# IMPORTANTE: false em producao
NEUROCARE_DEBUG=false

# Hosts permitidos: coloque o IP/dominio da sua VPS
NEUROCARE_ALLOWED_HOSTS=SEU_IP_DA_VPS,SEU_DOMINIO.com,backend,localhost

# Banco de dados
POSTGRES_DB=neurocare_db
POSTGRES_USER=neurocare_user
POSTGRES_PASSWORD=SENHA_FORTE_AQUI_MIN_16_CHARS
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# CORS: coloque o dominio/IP da VPS
CORS_ALLOWED_ORIGINS=http://SEU_IP_DA_VPS,http://SEU_DOMINIO.com,https://SEU_DOMINIO.com
```

### 5.3 Gerar a SECRET_KEY

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
# Copie o resultado e cole no NEUROCARE_SECRET_KEY do .env
```

### 5.4 Gerar senha forte para o banco

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(24))"
# Copie o resultado e cole no POSTGRES_PASSWORD do .env
```

---

## 6. Configurar docker-compose para producao

### 6.1 Criar docker-compose.prod.yml

```bash
nano docker-compose.prod.yml
```

Cole o conteudo abaixo:

```yaml
services:
  postgres:
    image: postgres:16
    restart: always
    env_file: .env
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./docker/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build: ./backend
    restart: always
    env_file: .env
    environment:
      POSTGRES_HOST: postgres
      DJANGO_SUPERUSER_USERNAME: admin
      DJANGO_SUPERUSER_PASSWORD: NeuroCare@Admin2026
      DJANGO_SUPERUSER_EMAIL: admin@neurocare.local
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - media_data:/app/media
    command: >
      sh -c "python manage.py migrate --noinput &&
             python manage.py createsuperuser --noinput 2>/dev/null || true &&
             python manage.py seed_test_users 2>/dev/null || true &&
             gunicorn neurocare_project.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120"

  frontend:
    build: ./frontend
    restart: always
    depends_on:
      - backend
    ports:
      - "80:80"

volumes:
  pgdata:
  media_data:
```

**Diferencas do desenvolvimento:**
- `restart: always` — containers reiniciam automaticamente
- Sem portas expostas para postgres (5432) e backend (8000) — so acessiveis internamente
- Frontend na porta 80 (HTTP padrao)
- Volume persistente para media (laudos PDF)
- env_file carrega do .env
- Timeout maior no gunicorn (120s)
- Senha do admin mais segura

---

## 7. Build e deploy

### 7.1 Construir as imagens

```bash
cd /home/neurocare/neurocare
docker compose -f docker-compose.prod.yml build
```

### 7.2 Subir a aplicacao

```bash
docker compose -f docker-compose.prod.yml up -d
```

cd /home/neurocare/neurocare
docker compose -f docker-compose.prod.yml down -v
docker compose -f docker-compose.prod.yml up -d

### 7.3 Verificar se tudo subiu

```bash
docker compose -f docker-compose.prod.yml ps
```

Deve mostrar 3 containers (postgres, backend, frontend) com status "Up".

### 7.4 Ver logs do backend

```bash
docker compose -f docker-compose.prod.yml logs -f backend
```

Deve mostrar "Starting gunicorn" sem erros. Ctrl+C para sair.

### 7.5 Testar acesso

```bash
# API
curl http://localhost/api/

# Frontend
curl -s -o /dev/null -w "%{http_code}" http://localhost/
# Deve retornar 200
```

---

## 8. Acessar a aplicacao

Abra no navegador:

```
http://SEU_IP_DA_VPS
```

Login inicial:
- **Usuario:** admin
- **Senha:** NeuroCare@Admin2026

**IMPORTANTE:** Troque a senha do admin apos o primeiro login.

---

## 9. HTTPS com Let's Encrypt (recomendado)

Se tiver um dominio apontando para a VPS:

### 9.1 Instalar Certbot

```bash
sudo apt install -y certbot
```

### 9.2 Parar o frontend temporariamente

```bash
docker compose -f docker-compose.prod.yml stop frontend
```

### 9.3 Gerar certificado

```bash
sudo certbot certonly --standalone -d SEU_DOMINIO.com
```

### 9.4 Criar nginx.prod.conf com SSL

```bash
nano frontend/nginx.prod.conf
```

```nginx
server {
    listen 80;
    server_name SEU_DOMINIO.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name SEU_DOMINIO.com;

    ssl_certificate /etc/letsencrypt/live/SEU_DOMINIO.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/SEU_DOMINIO.com/privkey.pem;

    root /usr/share/nginx/html;
    index index.html;

    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /media/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
    }

    location /admin/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
    }

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

### 9.5 Atualizar docker-compose.prod.yml para SSL

No servico `frontend`, adicionar volumes para os certificados e as portas 443:

```yaml
  frontend:
    build: ./frontend
    restart: always
    depends_on:
      - backend
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /etc/letsencrypt:/etc/letsencrypt:ro
      - ./frontend/nginx.prod.conf:/etc/nginx/conf.d/default.conf:ro
```

### 9.6 Rebuild e reiniciar

```bash
docker compose -f docker-compose.prod.yml up -d --build frontend
```

### 9.7 Renovacao automatica do certificado

```bash
sudo crontab -e
```

Adicione:

```
0 3 1 * * certbot renew --quiet && docker compose -f /home/neurocare/neurocare/docker-compose.prod.yml restart frontend
```

---

## 10. Firewall

```bash
# Permitir SSH, HTTP e HTTPS
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
sudo ufw status
```

---

## 11. Backup do banco de dados

### 11.1 Backup manual

```bash
docker compose -f docker-compose.prod.yml exec postgres pg_dump -U neurocare_user neurocare_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

### 11.2 Backup automatico (cron diario)

```bash
mkdir -p /home/neurocare/backups
crontab -e
```

Adicione:

```
0 2 * * * cd /home/neurocare/neurocare && docker compose -f docker-compose.prod.yml exec -T postgres pg_dump -U neurocare_user neurocare_db > /home/neurocare/backups/backup_$(date +\%Y\%m\%d).sql && find /home/neurocare/backups -mtime +30 -delete
```

Isso faz backup diario as 2h e mantem os ultimos 30 dias.

### 11.3 Restaurar backup

```bash
cat backup_20260626.sql | docker compose -f docker-compose.prod.yml exec -T postgres psql -U neurocare_user neurocare_db
```

---

## 12. Atualizacao da aplicacao

Quando houver novas versoes:

```bash
cd /home/neurocare/neurocare

# Puxar atualizacoes
git pull origin main

# Rebuild e restart
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d

# Verificar
docker compose -f docker-compose.prod.yml logs -f backend
```

---

## 13. Comandos uteis

```bash
# Ver status dos containers
docker compose -f docker-compose.prod.yml ps

# Ver logs em tempo real
docker compose -f docker-compose.prod.yml logs -f

# Reiniciar tudo
docker compose -f docker-compose.prod.yml restart

# Parar tudo
docker compose -f docker-compose.prod.yml down

# Parar e apagar dados (CUIDADO)
docker compose -f docker-compose.prod.yml down -v

# Entrar no container backend
docker compose -f docker-compose.prod.yml exec backend sh

# Criar novo superusuario
docker compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser

# Ver espaco em disco
docker system df
```

cd /home/neurocare/neurocare

# Puxar atualizações do git
git pull origin main

# Rebuild e restart
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d



---

## 14. Checklist de deploy

- [ ] VPS provisionada com Ubuntu 22.04/24.04
- [ ] Docker e Docker Compose instalados
- [ ] Repositorio clonado em /home/neurocare/neurocare
- [ ] Arquivo .env criado com SECRET_KEY, senha do banco e hosts
- [ ] docker-compose.prod.yml criado
- [ ] `docker compose -f docker-compose.prod.yml build` sem erros
- [ ] `docker compose -f docker-compose.prod.yml up -d` — 3 containers rodando
- [ ] http://SEU_IP funciona no navegador
- [ ] Login com admin funciona
- [ ] Firewall configurado (ufw)
- [ ] Backup automatico configurado (cron)
- [ ] (Opcional) HTTPS com Let's Encrypt configurado
- [ ] Senha do admin trocada apos primeiro login
