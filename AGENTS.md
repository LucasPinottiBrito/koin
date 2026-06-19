# AGENTS.md — koin

## 1. Project Identity

This repository contains **koin**, a personal finance agent focused on organizing a user's financial life directly inside Google Drive and Google Sheets.

koin is **not** a traditional personal finance platform. It is not intended to become an app like Organizze, Mobills, YNAB, Mint, or a full financial dashboard system.

The core product is:

> A personal finance agent that receives text, audio, spreadsheets, and PDFs, understands the user's intent, and organizes financial information directly in the user's own Google Drive spreadsheets.

The application exists to safely operate the agent.

The user experience is centered on conversation, not on dashboards, CRUD screens, or internal financial databases.

---

## 2. Mandatory Reading Before Coding

Before implementing, modifying, refactoring, or generating any feature, read:

```text
/docs/description.md
/docs/tech_specs.md
```

These two files are the source of truth for product direction and technical decisions.

If a requested implementation conflicts with these documents, stop and clarify before continuing.

Do not invent a broader product scope.

---

## 3. Product Rules

### 3.1 What koin is

koin is:

- a personal finance agent;
- a conversational interface for organizing financial data;
- a tool that creates, reads, and edits Google Drive and Google Sheets files;
- an assistant for inserting, editing, removing, importing, and organizing financial records in spreadsheets;
- a lightweight web application around an agent.

### 3.2 What koin is not

koin is not:

- a full personal finance platform;
- a financial dashboard app;
- an internal transaction management system;
- a budgeting platform with its own financial database;
- an Open Finance product;
- a banking integration product;
- an investment recommendation system;
- an ERP;
- an accounting system;
- a mobile-first finance tracker;
- a competitor to Organizze, Mobills, or similar apps.

Do not add features that push koin toward a traditional finance app unless explicitly requested and documented.

---

## 4. Core Technical Principle

The central technical rule is:

> The AI interprets and proposes. The backend validates, executes, and records.

The agent may understand the user's request, extract data, map columns, propose actions, and decide which tool should be used.

The agent must not directly perform uncontrolled operations.

All external actions must be executed through backend-controlled tools and adapters.

---

## 5. Data Ownership Rule

The user's financial data belongs in the user's Google Drive.

The application database must not become the primary store for the user's financial life.

PostgreSQL stores operational data only:

- users;
- Google integrations;
- Drive resources;
- agent sessions;
- messages;
- agent actions;
- jobs;
- category rules;
- user preferences.

PostgreSQL must not store a full transaction ledger, budget system, goals system, account system, credit card system, or financial dashboard data.

MongoDB stores audit and processing records only:

- agent runs;
- audit events;
- document processing logs.

MongoDB is not the operational source of truth.

---

## 6. MVP Scope

The MVP must support:

- Google login;
- Google Drive connection;
- creation or selection of the `Koin` folder;
- creation or selection of a Google Sheets financial spreadsheet;
- chat with the agent;
- text input;
- audio input;
- upload of CSV files;
- upload of XLSX files;
- experimental PDF processing;
- spreadsheet structure analysis;
- insertion of rows;
- simple row edits;
- simple row removals;
- import preview before bulk insertion;
- confirmation for sensitive actions;
- simple undo for recent reversible actions;
- simple category rules;
- basic answers based on spreadsheet contents;
- action history;
- worker-based processing for long tasks.

Do not implement in the MVP:

- financial dashboards;
- advanced charts;
- internal transaction CRUD;
- Open Finance;
- banking integrations;
- investment recommendations;
- mobile app;
- full budgeting system;
- full goals system;
- multi-user workspaces;
- complex reports;
- websocket unless explicitly requested.

---

## 7. Required Stack

Use the stack defined in `/docs/tech_specs.md`.

### Frontend

```text
Next.js
TypeScript
Tailwind CSS
shadcn/ui
```

### Backend

```text
Python
FastAPI
Pydantic
SQLAlchemy
Alembic
```

### Databases

```text
PostgreSQL
MongoDB
```

### AI and Integrations

```text
OpenAI API
Google OAuth
Google Drive API
Google Sheets API
```

### Processing

```text
Python worker
PostgreSQL jobs table as initial queue
Polling for job progress
```

### Infrastructure

```text
Docker
Docker Compose
```

---

## 8. Backend Architecture

Follow this development model:

```text
Controller
↓
Use Case
↓
Repository / Adapter / Service
↓
Database or external integration
```

Workers should reuse use cases whenever possible.

The backend should be organized by technical type:

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

Do not place business logic in controllers.

Do not place Google API, OpenAI API, or MongoDB calls directly inside controllers.

Use adapters.

---

## 9. Layer Responsibilities

### Controllers

Controllers receive HTTP requests and return HTTP responses.

They may:

- validate request shape;
- resolve authenticated user;
- call a use case;
- return standardized responses.

They must not:

- contain business logic;
- call OpenAI directly;
- call Google APIs directly;
- call MongoDB directly;
- manipulate spreadsheets directly;
- contain prompts.

### Use Cases

Use cases coordinate application flows.

Examples:

- `connect_google_drive`
- `setup_koin_folder`
- `create_financial_sheet`
- `connect_existing_spreadsheet`
- `send_agent_message`
- `process_audio_input`
- `upload_document`
- `analyze_spreadsheet`
- `confirm_import`
- `insert_sheet_row`
- `edit_sheet_row`
- `delete_sheet_row`
- `undo_recent_action`

Use cases should be readable and explicit.

### Services

Services contain reusable application logic.

Examples:

- `AgentService`
- `SheetMappingService`
- `DocumentProcessingService`
- `CategoryRuleService`
- `ConfirmationService`
- `ActionHistoryService`

### Repositories

Repositories access PostgreSQL.

Examples:

- `UserRepository`
- `IntegrationRepository`
- `ResourceRepository`
- `SessionRepository`
- `MessageRepository`
- `ActionRepository`
- `JobRepository`
- `CategoryRuleRepository`
- `PreferenceRepository`

### Adapters

Adapters isolate external services.

Examples:

- `GoogleDriveAdapter`
- `GoogleSheetsAdapter`
- `OpenAIAdapter`
- `MongoAuditAdapter`
- `AudioTranscriptionAdapter`
- `PDFParserAdapter`
- `SpreadsheetParserAdapter`

### Agent Tools

Agent tools are controlled backend operations that the agent can call.

Examples:

- `create_koin_folder`
- `create_financial_spreadsheet`
- `read_spreadsheet`
- `map_sheet_structure`
- `append_sheet_rows`
- `update_sheet_rows`
- `delete_sheet_rows`
- `extract_transactions_from_file`
- `classify_transaction`
- `create_confirmation_request`

All agent tools must validate inputs before execution.

---

## 10. Agent Rules

The agent must operate through structured tools.

The agent can:

- understand text;
- understand transcribed audio;
- interpret financial documents;
- detect spreadsheet structures;
- map spreadsheet columns;
- classify transactions;
- propose spreadsheet changes;
- explain what happened;
- answer simple financial questions based on spreadsheet data.

The agent must not:

- execute arbitrary code;
- make uncontrolled Drive changes;
- write directly to spreadsheets without tool validation;
- store a complete internal transaction database;
- provide investment recommendations;
- silently perform bulk destructive operations;
- bypass confirmation for sensitive actions.

---

## 11. Confirmation Rules

Simple actions may be executed directly.

Examples:

- adding a clearly described expense;
- adding a clearly described income;
- answering a question based on the spreadsheet;
- inserting one simple row into the default sheet.

Sensitive actions require confirmation.

Examples:

- removing rows;
- editing multiple cells;
- importing a file;
- applying bulk changes;
- reorganizing a spreadsheet;
- changing headers;
- creating a copy of a spreadsheet;
- deleting or replacing data;
- processing a PDF with uncertain extraction.

When unsure, ask for confirmation.

---

## 12. Audio Input Rules

Audio must support more than one action in a single message.

Example:

```text
Hoje gastei R$ 30 com almoço, R$ 12 com café, R$ 80 de gasolina e recebi R$ 500 de um serviço.
```

The agent must split this into separate structured actions.

If the audio produces many actions or ambiguous commands, request confirmation before writing to the spreadsheet.

---

## 13. Document Processing Rules

Supported MVP formats:

```text
CSV
XLSX
PDF experimental
Google Sheets
```

CSV and XLSX should be treated as official MVP import formats.

PDF must be treated as experimental and should produce a preview before import.

All document imports must follow this flow:

```text
upload
↓
save file to Google Drive
↓
create processing job
↓
extract data
↓
map columns
↓
generate preview
↓
ask confirmation
↓
write confirmed rows to Google Sheets
↓
record action
```

Do not insert bulk imported data without preview and confirmation.

---

## 14. Spreadsheet Rules

The default spreadsheet created by koin must include:

```text
Transações
Categorias
Resumo
Histórico
```

The default `Transações` sheet should use simple columns:

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

Do not make the spreadsheet structure unnecessarily complex.

When connecting an existing spreadsheet:

1. read metadata;
2. identify sheets;
3. identify likely financial tables;
4. propose column mapping;
5. ask the user to confirm or correct the mapping;
6. save the mapping in resource metadata.

Do not assume all spreadsheets follow the koin default structure.

---

## 15. Database Rules

### PostgreSQL

Use PostgreSQL for operational data only.

Initial tables:

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

Do not add tables like:

```text
transactions
budgets
goals
accounts
credit_cards
financial_reports
```

unless the documentation is explicitly changed.

### MongoDB

Use MongoDB for:

```text
audit_events
agent_runs
document_processing_logs
```

MongoDB writes are best effort in the MVP.

A MongoDB write failure must not invalidate an already completed business operation.

Always produce structured technical logs for MongoDB failures.

Do not use MongoDB as the source of truth for current application state.

---

## 16. Security Rules

- Google tokens must be encrypted before being stored.
- Never log raw Google tokens.
- Never log full financial documents unnecessarily.
- Avoid storing sensitive financial data in PostgreSQL.
- Minimize sensitive data sent to AI models.
- Use only the Drive scopes required by the product.
- The application should work with files created by koin or files manually selected by the user.
- Do not request broad Drive access unless explicitly required and documented.
- Provide a way to disconnect Google integration.

---

## 17. Logging and Debugging

Every important operation should include correlation identifiers.

Use fields such as:

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

- request start/end;
- Google API failures;
- OpenAI failures;
- file parsing failures;
- job failures;
- confirmation flow errors;
- Mongo audit failures;
- spreadsheet write failures;
- duration of relevant operations.

Do not log complete financial data unless explicitly required for a controlled test fixture.

---

## 18. Testing Guidelines

Create tests for:

- use cases;
- repositories;
- adapters with mocks;
- agent tool validation;
- CSV parsing;
- XLSX parsing;
- PDF experimental parsing;
- spreadsheet column mapping;
- category rule matching;
- confirmation flows;
- job state transitions.

Use fixtures for imported files:

```text
tests/fixtures/csv/
tests/fixtures/xlsx/
tests/fixtures/pdf/
```

PDF tests should account for imperfect extraction.

---

## 19. Prompt Guidelines

Prompts must be centralized under:

```text
backend/src/prompts/
```

Prompts must be versioned.

Do not hardcode long prompts inside controllers, services, or adapters.

Prompt outputs should be structured whenever possible with Pydantic schemas.

The agent should prefer tool calls over free-form operational instructions.

---

## 20. Frontend Guidelines

The frontend should remain minimal.

Required areas:

- login page;
- onboarding for Google Drive connection;
- folder selection/creation;
- spreadsheet selection/creation;
- chat with agent;
- file upload;
- audio input;
- connected files view;
- action history;
- Drive settings.

Do not add:

- financial dashboard pages;
- graph-heavy screens;
- transaction CRUD pages;
- budgeting screens;
- investment pages;
- analytics screens.

The main product interface is the agent conversation.

---

## 21. Worker Guidelines

Workers handle long-running operations.

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

The frontend tracks job progress by polling.

Do not introduce Redis, Celery, Kafka, RabbitMQ, or WebSocket unless explicitly requested and documented.

---

## 22. Error Handling Rules

Use typed application errors.

Do not expose internal stack traces to the frontend.

Return user-friendly messages.

For agent actions, when an operation fails, the assistant response should explain:

- what failed;
- whether any data was changed;
- what the user can do next.

For partial changes, record the action as partial and explain the state clearly.

---

## 23. Documentation Rules

When changing product behavior, update:

```text
/docs/description.md
/docs/tech_specs.md
```

When changing development guidance, update:

```text
AGENTS.md
GEMINI.md
```

When adding important flows, document:

- purpose;
- endpoint or entry point;
- involved use case;
- involved adapters;
- confirmation behavior;
- audit behavior.

---

## 24. Non-Negotiable Constraints

The following constraints must be preserved:

1. koin is an agent, not a financial platform.
2. Google Drive and Google Sheets are the financial workspace.
3. PostgreSQL stores operational data only.
4. MongoDB stores audit and processing logs only.
5. The app must not create internal finance dashboards in the MVP.
6. The app must not create a full internal transaction database.
7. The AI must not bypass backend validation.
8. Sensitive or bulk spreadsheet changes require confirmation.
9. PDF support is experimental.
10. The product must stay simple.

If a task conflicts with these constraints, stop and ask for clarification.
