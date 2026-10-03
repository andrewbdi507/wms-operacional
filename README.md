# WMS Operacional

## Visão geral

Sistema de gestão de warehouse (WMS) para demonstração de operações logísticas e separação de pedidos. Este é um projeto de portfólio demonstrativo com dados fictícios, criado para apresentar habilidades de desenvolvimento full-stack com FastAPI, SQLAlchemy e Docker.

O sistema demonstra fluxos de controle de estoque, separação de pedidos e gestão de produtos em ambiente warehouse.

## Principais funcionalidades

- **Cadastro de produtos**: CRUD completo de produtos com SKU e EAN-13
- **Controle de estoque**: Sistema de quantidade e reserva de produtos
- **Gestão de usuários**: Perfis de acesso (admin, operador, gerente) com permissões diferenciadas
- **Operações de separação**: Fluxo de criação e processamento de pedidos
- **Reservas de produtos**: Sistema de redução de estoque ao criar pedidos
- **Relatórios básicos**: Visão geral de atividades e status do sistema

## Fluxo operacional (DEMO)

1. Acessar a aplicação e realizar login com credenciais de demonstração
2. Navegar até a área de produtos para visualizar/listar itens em estoque
3. Criar novos produtos com SKU e EAN únicos
4. Simular criação de pedidos, que automaticamente reduzem o estoque disponível
5. Visualizar histórico de pedidos e status de separação
6. Acessar painel de controle para visão geral das operações

## Stack

- **Backend**: FastAPI (Python 3.13), SQLAlchemy 2.x, Alembic (migrations)
- **Banco de dados**: SQLite (demonstração) / PostgreSQL (produção)
- **Autenticação**: JWT (JSON Web Token) com campos de senha no modelo User
- **Testes**: pytest com 5 testes unitários passando
- **Container**: Docker configurado (Dockerfile presente)

## Arquitetura

Aplicação FastAPI com estrutura modular:
- `app/main.py`: Roteamento e inicialização da aplicação
- `app/models.py`: Definição de modelos SQLAlchemy (Account, User, Product, EAN, SKU, Order, Transaction)
- `app/database.py`: Configuração de engine e sessão do banco de dados
- `app/seed_com_codigos_fixos.py`: Script de seed com dados fictícios para demonstração
- `app/api/`: Endpoints da API REST

## Banco de dados

- Modelos definidos em `app/models.py` com SQLAlchemy 2.x
- Migrations via Alembic em `alembic/versions/`
- Script de seed `app/seed_com_codigos_fixos.py` popula dados fictícios para DEMO
- Estrutura suporta PostgreSQL para produção

## Segurança

- Autenticação via JWT com senhas hashed no modelo User
- Campos de senha apenas no modelo de criação de usuário (UserCreate)
- Variáveis de ambiente em `.env.example` (sem credenciais reais)
- Controle de acesso por perfil (admin, operador, gerente)
- Nenhuma chave API ou token real armazenado no código

## Testes

- **5 testes unitários passando** (test_simple.py)
- Cobertura: endpoints root, health, criação de produto, criação de usuário, criação de ordem
- Testes executados via: `python -m pytest tests/ -v`
- Inclui testes de: autenticação básica, permissões, criação e listagem de recursos

## Como executar localmente

1. Criar ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Instalar dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configurar variáveis de ambiente:
   ```bash
   cp .env.example .env
   # Editar .env com as configurações locais
   ```

4. Executar migrations:
   ```bash
   alembic upgrade head
   ```

5. Executar seed (criar dados de demo):
   ```bash
   python app/seed_com_codigos_fixos.py
   ```

6. Iniciar aplicação:
   ```bash
   uvicorn app.main:app --reload
   ```



## Migrations

- `alembic upgrade head`: Aplicar todas as migrations pendentes
- `alembic downgrade base`: Reverter para estado base
- Migration `alembic/versions/20260928_001_initial.py`: Cria todas as tabelas (accounts, users, products, eans, skus, orders, transactions)
- Migration `head` é suficiente para criar o schema necessário para a DEMO

## Estrutura do projeto

```
wms-operacional/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── seed_com_codigos_fixos.py
│   └── api/
│       ├── __init__.py
│       ├── auth.py
│       ├── permissions.py
│       └── __init__.py
├── alembic/
│ ├── env.py
│ └── versions/
│   └── 20260928_001_initial.py
├── tests/
│   ├── test_simple.py
│   └── test_basic.py
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── SECURITY.md
├── LIMITACOES_CONHECIDAS.md
└── README.md
```

## Limitações conhecidas

- Dados fictícios: Este projeto utiliza dados simulados para demonstração e não deve ser usado em produção sem adequações
- Banco SQLite: Usado para demonstração; para produção recomenda-se PostgreSQL
- Funcionalidades limitadas: Algumas features avançadas de WMS podem não estar disponíveis na versão demo
- Desempenho: Não otimizado para alto volume de transações
- Integrações: Integrações com Mercado Livre e Olist são simuladas para demonstração

## Próximos passos

- **Funcionalidades existentes**: Separação de pedidos, controle de estoque, gestão de usuários, reservas de produtos, endpoints API REST
- **Possíveis evoluções futuras**: Integrações reais com marketplaces, dashboard avançado, autenticação OAuth2, relatórios detalhados, API pública versões

## Observação

Todos os dados da aplicação (produtos, EANs, SKUs, usuários, pedidos) são fictícios e destinados exclusivamente à demonstração deste projeto de portfólio. Nenhum dado real ou sensível está incluído.

---

Desenvolvido como projeto de demonstração de habilidades técnicas em FastAPI, SQLAlchemy e desenvolvimento web moderno.
