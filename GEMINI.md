# GEMINI.md — koin

## 1. Project Context

You are working on **koin**, a personal finance agent.

koin helps users organize their financial life directly in their own Google Drive and Google Sheets files.

The product is intentionally simple.

It is not a traditional finance app.

It is not a dashboard platform.

It is not an internal financial database.

It is an agent-centered application.

The core idea is:

> The user talks to koin. koin organizes the user's finances in Google Drive spreadsheets.

---

## 2. Required Documents

Before making implementation decisions, read:

```text
/docs/description.md
/docs/tech_specs.md
```

These files define the product and the technical specification.

Use them as the source of truth.

Do not broaden the scope beyond them.

---

## 3. Important Product Boundary

Do not build koin as:

- Organizze;
- Mobills;
- YNAB;
- Mint;
- a banking app;
- an Open Finance app;
- an investment assistant;
- a financial dashboard;
- an ERP;
- an accounting system;
- a complete budgeting system.

Build koin as:

- a web interface around an agent;
- a Google Drive and Google Sheets organizer;
- a conversational financial assistant;
- a controlled tool executor for spreadsheet operations.

---

## 4. Main User Experience

The main user experience is a chat.

The user can send:

- text;
- audio;
- CSV files;
- XLSX files;
- experimental PDFs;
- selected Google Sheets files.

The agent can:

- create a `Koin` folder;
- create a default financial spreadsheet;
- connect an existing spreadsheet;
- read spreadsheet structures;
- map columns;
- insert rows;
- edit rows;
- remove rows;
- import transactions from files;
- classify transactions;
- answer simple questions based on spreadsheet data;
- suggest simple organization and saving actions;
- explain what it changed.

The agent must always operate through controlled backend tools.

---

## 5. Golden Rule

Follow this rule throughout the project:

> AI interprets and proposes. Backend validates, executes, and records.

Never let the AI directly perform uncontrolled file, sheet, database, or external API operations.

---

## 6. MVP Scope

The MVP includes:

```text
Google login
Google Drive connection
Koin folder setup
Google Sheets setup
Agent chat
Text input
Audio input
CSV upload
XLSX upload
Experimental PDF upload
Spreadsheet reading
Spreadsheet mapping
Row insertion
Simple row editing
Simple row removal
Import preview
Confirmation for sensitive actions
Simple undo for recent reversible actions
Simple category rules
Action history
MongoDB audit logs
PostgreSQL operational data
Worker for long jobs
Polling for job progress
```

The MVP excludes:

```text
Financial dashboards
Advanced charts
Internal transaction CRUD
Internal transaction ledger
Budgeting system
Goals system
Open Finance
Banking integration
Investment recommendation
Mobile app
Multi-user workspace
Complex reports
WebSocket
Server-Sent Events
Transactional outbox
```

---

## 7. Architecture

Use a simple monolithic backend.

The chosen development model is:

```text
Controller
↓
Use Case
↓
Repository / Adapter / Service
↓
Database or external integration
```

The backend is organized by technical type:

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
└── pyproject.toml
```

Keep the architecture readable.

Avoid excessive abstractions.

---

## 8. Stack

Use the defined stack.

Frontend:

```text
Next.js
TypeScript
Tailwind CSS
shadcn/ui
```

Backend:

```text
Python
FastAPI
Pydantic
SQLAlchemy
Alembic
```

Databases:

```text
PostgreSQL
MongoDB
```

AI and Google:

```text
OpenAI API
Google OAuth
Google Drive API
Google Sheets API
```

Processing:

```text
Python worker
PostgreSQL jobs table
Polling for progress
```

Infra:

```text
Docker
Docker Compose
```

Do not introduce new infrastructure unless explicitly requested.

---

## 9. Backend Rules

Controllers must not contain business logic.

Controllers must not call:

- OpenAI directly;
- Google APIs directly;
- MongoDB directly;
- spreadsheet mutation logic directly.

Use cases coordinate flows.

Repositories access PostgreSQL.

Adapters access external services.

Services contain reusable application logic.

Agent tools expose safe, structured operations to the AI.

Workers process long tasks and should reuse use cases when possible.

---

## 10. Database Rules

### PostgreSQL

PostgreSQL stores operational data.

Allowed core tables:

```text
users
google_integrations
drive_resources
agent_sessions
agent_messages
agent_actions
jobs
category_rules
user_preferences
```

Do not create these tables in the MVP:

```text
transactions
budgets
goals
accounts
credit_cards
financial_reports
```

The user's financial records should remain in Google Sheets.

### MongoDB

MongoDB stores detailed logs and audit records.

Collections:

```text
audit_events
agent_runs
document_processing_logs
```

MongoDB writes are best effort.

If MongoDB fails, do not automatically fail an already completed business operation.

Log the Mongo failure with structured technical logs.

Do not use MongoDB as the source of truth for current application state.

---

## 11. Google Drive and Sheets Rules

The application works with:

- files created by koin;
- files manually selected by the user.

Do not request broad Drive access unless the documentation explicitly changes.

The default Drive folder name is:

```text
Koin
```

The default spreadsheet tabs are:

```text
Transações
Categorias
Resumo
Histórico
```

The default `Transações` columns are:

```text
Data
Descrição
Tipo
Valor
Categoria
Forma de pagamento
Origem
Observações
Criado por
Criado em
```

Do not overcomplicate the spreadsheet structure.

When using an existing spreadsheet, analyze it first and ask the user to confirm the column mapping.

---

## 12. Agent Tool Rules

The agent should use tools such as:

```text
create_koin_folder
create_financial_spreadsheet
read_spreadsheet_metadata
read_sheet_rows
map_sheet_structure
append_sheet_rows
update_sheet_rows
delete_sheet_rows
parse_csv
parse_xlsx
parse_pdf_experimental
extract_financial_rows
generate_import_preview
classify_transaction
get_user_category_rules
save_category_rule
create_confirmation_request
record_agent_action
```

Every tool must have:

- typed input schema;
- typed output schema;
- validation;
- predictable errors;
- audit behavior where relevant.

The agent should never invent direct spreadsheet operations outside the tool interface.

---

## 13. Confirmation Rules

Do not ask for confirmation for every small action.

A clear single transaction insertion can execute directly.

Ask for confirmation when the action is sensitive.

Sensitive actions include:

- deleting rows;
- deleting multiple rows;
- editing many cells;
- importing documents;
- applying bulk changes;
- reorganizing a spreadsheet;
- changing headers;
- creating a modified copy of a spreadsheet;
- replacing data;
- extracting uncertain data from a PDF.

If a request is ambiguous, ask a clarifying question or request confirmation.

---

## 14. Audio Rules

Audio input must support multiple actions in the same recording.

Example:

```text
Hoje gastei R$ 30 com almoço, R$ 12 com café, R$ 80 de gasolina e recebi R$ 500 de um serviço.
```

The system should:

1. transcribe the audio;
2. extract multiple financial actions;
3. validate each action;
4. execute simple actions or ask confirmation for larger batches;
5. respond with a clear summary.

---

## 15. Document Rules

CSV and XLSX are official MVP formats.

PDF is experimental.

For any document import:

1. save the file to Google Drive;
2. create a processing job;
3. parse the document;
4. extract possible financial rows;
5. create an import preview;
6. ask confirmation;
7. write confirmed rows to the spreadsheet;
8. record the action.

Do not import document rows in bulk without preview.

---

## 16. Prompt Rules

Prompts must be stored under:

```text
backend/src/prompts/
```

Prompts must be versioned.

Do not hardcode important prompts in controllers, use cases, or adapters.

Prefer structured outputs with Pydantic schemas.

Prefer agent tool calls over free-form instructions.

---

## 17. Frontend Rules

The frontend is minimal.

Required screens or areas:

- login;
- Google Drive onboarding;
- folder setup;
- spreadsheet setup;
- chat;
- file upload;
- audio input;
- connected files;
- action history;
- Drive settings.

Do not create:

- finance dashboard pages;
- advanced charts;
- internal transaction management pages;
- budgeting pages;
- investment pages;
- analytics pages.

The chat is the product.

---

## 18. Worker Rules

Use workers for:

- audio processing;
- CSV processing;
- XLSX processing;
- PDF processing;
- spreadsheet analysis;
- import preview generation;
- bulk imports;
- spreadsheet organization.

Use the PostgreSQL `jobs` table as the initial queue.

Use polling for job status.

Do not add Redis, Celery, Kafka, RabbitMQ, WebSocket, or Server-Sent Events unless explicitly requested.

---

## 19. Security Rules

- Encrypt Google tokens.
- Never log raw tokens.
- Minimize financial data stored internally.
- Minimize financial data sent to AI models.
- Do not store full financial ledgers in PostgreSQL.
- Avoid logging full financial documents.
- Use least-privilege Google scopes.
- Allow the user to disconnect Google integration.

---

## 20. Logging Rules

Every relevant operation should include:

```text
request_id
user_id
session_id
message_id
action_id
job_id
resource_id
agent_run_id
```

Log:

- Google failures;
- OpenAI failures;
- parsing errors;
- spreadsheet write errors;
- job errors;
- audit errors;
- confirmation flow issues;
- operation duration.

Do not log sensitive financial data unnecessarily.

---

## 21. Testing Rules

Create tests for:

- use cases;
- repository behavior;
- adapter mocks;
- agent tool validation;
- CSV parsing;
- XLSX parsing;
- PDF experimental parsing;
- spreadsheet mapping;
- category rules;
- confirmation flows;
- job transitions;
- undo behavior.

Use fixture files under:

```text
tests/fixtures/csv/
tests/fixtures/xlsx/
tests/fixtures/pdf/
```

Keep fixtures anonymized.

---

## 22. Code Quality Rules

- Prefer clear code over clever abstractions.
- Keep functions small.
- Keep use cases readable.
- Avoid generic architecture that hides product behavior.
- Use typed schemas.
- Use explicit errors.
- Do not duplicate business logic between API and worker.
- Do not scatter integrations across the codebase.
- Do not silently swallow external API errors.
- Do not silently perform destructive operations.

---

## 23. Implementation Warnings

Stop and ask for clarification if a task requires:

- creating internal transaction tables;
- creating dashboards;
- adding banking integrations;
- adding Open Finance;
- adding investment features;
- adding complex budget or goals systems;
- bypassing confirmation for bulk edits;
- storing full financial data internally;
- granting broad Drive access;
- replacing Google Sheets as the financial workspace.

These likely violate the current product scope.

---

## 24. Documentation Rules

Update documentation when behavior changes.

Product and technical documentation:

```text
/docs/description.md
/docs/tech_specs.md
```

Agent guidance:

```text
AGENTS.md
GEMINI.md
```

Keep documentation aligned with implementation.

---

## 25. Final Reminder

koin must stay simple.

The product is not:

```text
app financeiro + dashboards + banco próprio
```

The product is:

```text
agente + Google Drive + Google Sheets
```

When in doubt, preserve the agent-centered design.
