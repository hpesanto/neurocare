-- create_paciente.sql
-- Cria a tabela `paciente` em PostgreSQL com id do tipo UUID gerado automaticamente.
-- Requisitos: extensão pgcrypto (fornece gen_random_uuid()).
-- Execute com: psql -h <host> -U <user> -d <db> -f create_paciente.sql
-- Habilita extensão pgcrypto (gera gen_random_uuid)
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Opcional: dropar tabela existente (descomente se quiser recriar do zero)
-- DROP TABLE IF EXISTS paciente;
CREATE TABLE IF NOT EXISTS paciente (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cpf VARCHAR(20),
    nome VARCHAR(255) NOT NULL,
    RG VARCHAR(50),
    genero text [],
    estado_civil VARCHAR(50),
    profissao VARCHAR(100),
    tel_1 VARCHAR(50),
    tel_2 VARCHAR(50),
    email VARCHAR(254),
    logradouro VARCHAR(255),
    num_fachada VARCHAR(50),
    complemento VARCHAR(255),
    bairro VARCHAR(255),
    municipio VARCHAR(255),
    uf CHAR(2),
    cep VARCHAR(20),
    contato_emergencia VARCHAR(255),
    tel_contato_emergencia VARCHAR(50),
    parentesco_contato_emergencia VARCHAR(100)
);

-- Índices sugeridos
CREATE INDEX IF NOT EXISTS paciente_nome_idx ON paciente (lower(nome));

CREATE INDEX IF NOT EXISTS paciente_cpf_idx ON paciente (cpf);

-- Observação:
-- 1) gen_random_uuid() vem da extensão pgcrypto. Se preferir uuid-ossp, substitua por uuid_generate_v4()
--    e habilite: CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- 2) Não existe "autoincrement" num UUID no sentido numérico. A função acima gera um UUID por row.
-- 3) Se você usa Django, no model defina:
--     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
--    e ajuste Meta.managed conforme desejar (managed=True se quiser que Django crie a tabela via migrations).
-- Exemplos de conversão de dados legados (quando houver valores string em genero):
-- UPDATE paciente SET genero = ARRAY[ genero::text ] WHERE genero IS NOT NULL AND pg_typeof(genero)::text NOT LIKE 'text[]' AND genero::text NOT LIKE '{%';
-- End of file