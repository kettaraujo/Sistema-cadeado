# Sistema de Consulta e Abertura de Cadeado

Projeto desenvolvido em **Python com Django** para consulta de cadeados em uma API externa e envio de comando de abertura via integração HTTP.

O sistema possui uma tela simples onde o usuário informa o ID do cadeado. Caso o cadeado seja encontrado na API, seus dados principais são exibidos e o botão de abertura é habilitado.

---

## Objetivo do Projeto

O objetivo deste projeto é praticar conceitos de desenvolvimento web com Django e integração com APIs externas, incluindo:

- Criação de projeto Django;
- Criação de app;
- Uso de templates HTML;
- Consumo de API externa com `requests`;
- Uso de variáveis de ambiente com `.env`;
- Implementação de cache local;
- Separação de responsabilidades com `forms.py`, `views.py` e `services.py`;
- Envio de comandos para uma API externa.

---

## Funcionalidades

- Buscar cadeado pelo ID;
- Consultar dados em uma API externa;
- Verificar se o cadeado existe no retorno da API;
- Exibir informações do cadeado encontrado;
- Enviar comando de abertura do cadeado;
- Exibir mensagem de sucesso ou erro;
- Utilizar cache local de 5 minutos para reduzir chamadas à API.

---

## Tecnologias Utilizadas

- Python
- Django
- Requests
- Python Decouple
- Bootstrap
- HTML
- Git/GitHub

---

## Estrutura do Projeto

```text
cadeado/
├── consulta/
│   ├── templates/
│   │   └── consulta/
│   │       └── buscar.html
│   ├── forms.py
│   ├── services.py
│   ├── urls.py
│   └── views.py
├── setup/
│   ├── settings.py
│   └── urls.py
├── .env.example
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt