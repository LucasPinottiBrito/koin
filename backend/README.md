# koin backend

Base inicial do backend do **koin**, um agente de finanças pessoais que organiza informações financeiras diretamente em arquivos do Google Drive e Google Sheets do usuário.

Esta base ainda **não** implementa autenticação, agente, Google Drive/Sheets, importação de documentos ou regras de negócio financeiras. O objetivo é oferecer uma fundação simples para continuidade do desenvolvimento.

## O que foi criado

- Aplicação FastAPI funcional em `src/main.py`.
- Endpoint `GET /health` em `src/controllers/health.py`.
- Carregamento de variáveis de ambiente com Pydantic Settings em `src/config/settings.py`.
- Configuração inicial de logs em `src/logging/config.py`.
- Conexão inicial com PostgreSQL via SQLAlchemy em `src/database/postgres.py`.
- Adapter inicial de MongoDB em `src/adapters/mongo_adapter.py`.
- Processo inicial de worker em `src/workers/main.py`, preparado para polling futuro da tabela `jobs` no PostgreSQL.
- Estrutura de camadas preparada para controllers, use cases, repositories, adapters, services, workers, prompts e agent tools.
- Dockerfile compartilhado por API e worker.
- Docker Compose local com `backend-api`, `worker`, `postgres` e `mongodb`.
- Teste automatizado do endpoint de healthcheck.

## Estrutura

```text
backend/
├── src/
│   ├── controllers/
│   ├── use_cases/
│   ├── services/
│   ├── repositories/
│   ├── adapters/
│   ├── models/
│   ├── schemas/
│   ├── workers/
│   ├── prompts/
│   ├── agent_tools/
│   ├── database/
│   ├── config/
│   ├── security/
│   ├── logging/
│   └── main.py
├── tests/
├── migrations/
├── pyproject.toml
├── Dockerfile
└── README.md
```

## Variáveis de ambiente

Copie o arquivo de exemplo na raiz do repositório antes de subir os serviços:

```bash
cp .env.example .env
```

Principais variáveis usadas pelo backend:

| Variável | Descrição |
| --- | --- |
| `APP_ENV` | Ambiente de execução. |
| `APP_NAME` | Nome exibido pela aplicação FastAPI. |
| `API_PORT` | Porta local publicada para a API. |
| `DATABASE_URL` | URL SQLAlchemy para PostgreSQL. |
| `MONGO_URL` | URL de conexão autenticada do MongoDB. |
| `MONGO_DATABASE` | Database MongoDB para auditoria e logs futuros. |
| `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REDIRECT_URI` | Configuração futura de OAuth Google. |
| `OPENAI_API_KEY` | Chave futura da OpenAI API. |
| `TOKEN_ENCRYPTION_KEY` | Chave futura para criptografia de tokens Google. |

## Subir a aplicação com Docker Compose

Na raiz do repositório:

```bash
cp .env.example .env
docker compose up --build
```

Serviços criados:

- `backend-api`: executa FastAPI em `http://localhost:${API_PORT}`.
- `worker`: usa a mesma imagem/base do backend e executa `python -m src.workers.main`.
- `postgres`: banco operacional do koin.
- `mongodb`: armazenamento futuro de auditoria e logs de processamento.

Healthcheck da API:

```bash
curl http://localhost:8000/health
```

## Rodar migrations

As migrations ainda não criam tabelas de negócio; o Alembic foi preparado para quando os modelos operacionais forem adicionados.

Com os serviços do Compose em execução:

```bash
docker compose run --rm backend-api alembic upgrade head
```

Localmente, sem Docker:

```bash
cd backend
alembic upgrade head
```

## Rodar testes

Com Docker Compose:

```bash
docker compose run --rm backend-api pytest
```

Localmente:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Rodar o worker

Com Docker Compose, o worker sobe junto com os demais serviços:

```bash
docker compose up worker
```

Também é possível executar um processo descartável:

```bash
docker compose run --rm worker
```

Localmente:

```bash
cd backend
python -m src.workers.main
```

O worker não usa Redis, Celery, Kafka, RabbitMQ ou outro broker. A fila inicial do koin será implementada sobre a tabela `jobs` no PostgreSQL.

## Diretrizes preservadas

- Controllers não contêm regra de negócio.
- O healthcheck delega coordenação para um use case.
- MongoDB fica isolado em adapter.
- PostgreSQL fica isolado no módulo de database, pronto para repositories.
- Nenhuma tabela interna de transações, orçamento, metas, contas ou cartões foi criada.
- Nenhum agente ou autenticação foi implementado nesta etapa.
