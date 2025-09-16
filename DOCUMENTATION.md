# NeuroCare - Estrutura inicial do projeto

Este repositório contém a estrutura inicial de uma aplicação Django modular. O objetivo é ter uma base onde podemos adicionar módulos (apps) gradualmente. Abaixo estão as peças principais e instruções.

Estrutura criada:

- `neurocare_project/` - pacote principal do Django com settings, urls, wsgi e utilitários.
- `accounts/` - app responsável por autenticação (login/logout) e perfil.
- `templates/` - templates base e templates do `accounts`.
- `menu_config.py` - arquivo central onde o menu da aplicação é definido.
- `manage.py` - utilitário padrão do Django.

Como o menu funciona

O arquivo `neurocare_project/menu_config.py` exporta uma lista `MENU` com dicionários. Cada item tem as chaves:

- `title`: texto mostrado no menu
- `url`: caminho para o link
- `permissions` (opcional): lista de permissions Django necessárias para ver o item

Exemplo:

    MENU = [
        {'title': 'Home', 'url': '/'},
        {'title': 'Pacientes', 'url': '/pacientes/'},
        {'title': 'Agendamentos', 'url': '/agendamentos/', 'permissions': ['accounts.view_agendamento']},
    ]

O `neurocare_project/context_processors.py` fornece os itens filtrados pela sessão do usuário para os templates como `MENU_ITEMS`.

Adicionar novos módulos (apps)

1. Criar a app com `python manage.py startapp nome_app`.
2. Adicionar `nome_app` em `INSTALLED_APPS` em `neurocare_project/settings.py`.
3. Criar views, urls e templates; incluir `include('nome_app.urls')` em `neurocare_project/urls.py`.

Como editar o menu

Edite `neurocare_project/menu_config.py` e reinicie o servidor de desenvolvimento para ver as alterações.

Segurança e produção

- Troque `SECRET_KEY` em `neurocare_project/settings.py` por uma chave segura.
- Ajuste `DEBUG=False` e `ALLOWED_HOSTS` antes de colocar em produção.
