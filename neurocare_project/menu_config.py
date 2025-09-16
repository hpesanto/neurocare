# Menu configuration: edit this file to add menu items.
# Each item is a dict with: 'title', 'url' and optional 'permissions' (list of permission strings)

MENU = [
    {"title": "Home", "url": "/"},
    {
        "title": "Cadastro",
        "url": "#",
        "permissions": ["accounts.add_paciente"],
        "children": [
            {
                "title": "Pacientes",
                "url": "/cadastro/pacientes/",
                "permissions": ["accounts.view_paciente"],
            },
            {
                "title": "Profissionais",
                "url": "/cadastro/profissionais/",
                "permissions": ["accounts.view_profissional"],
            },
            {
                "title": "Usuários",
                "url": "/cadastro/usuarios/",
                "permissions": ["auth.view_user"],
            },
        ],
    },
    {
        "title": "Agendamentos",
        "url": "/agendamentos/",
        "permissions": ["accounts.view_agendamento"],
    },
]
