# koin — Especificação Técnica da Aplicação

## 1. Visão geral técnica

O **koin** será uma aplicação web baseada em um agente de IA para organização de finanças pessoais diretamente no Google Drive do usuário.

A aplicação não será uma plataforma financeira tradicional. Ela não terá dashboard financeiro próprio, banco interno de transações, telas complexas de orçamento, CRUD financeiro completo ou modelo de gestão semelhante a aplicativos como Organizze, Mobills ou sistemas de controle financeiro tradicionais.

O núcleo da aplicação será um agente que conversa com o usuário e executa ações controladas sobre arquivos e planilhas do Google Drive.

O usuário poderá interagir com o koin por:

* texto;
* áudio;
* upload de documentos;
* planilhas existentes;
* PDFs financeiros simples ou moderadamente estruturados.

O agente deverá ser capaz de:

* criar pasta no Google Drive;
* criar planilhas financeiras;
* localizar planilhas existentes selecionadas pelo usuário;
* ler estruturas de planilhas;
* interpretar comandos financeiros;
* inserir linhas;
* editar linhas;
* remover linhas;
* organizar colunas e abas;
* processar documentos enviados;
* extrair transações de planilhas, CSVs, XLSX e PDFs;
* classificar transações com ajuda de IA;
* salvar preferências simples do usuário;
* responder perguntas simples com base nos dados da planilha;
* explicar o que foi feito.

A aplicação deverá manter a ideia central:

> O koin não armazena a vida financeira do usuário. O koin organiza a vida financeira do usuário nas próprias planilhas do Google Drive.

## 2. Objetivo da aplicação

O objetivo técnico da aplicação é fornecer uma interface segura, simples e confiável para que um agente de IA possa manipular arquivos financeiros do usuário no Google Drive.

O produto deve permitir que o usuário execute ações financeiras por linguagem natural, sem precisar editar manualmente planilhas.

Exemplos:

* “Adicione R$ 42,90 de mercado hoje.”
* “Registre que recebi R$ 3.500 de salário.”
* “Organize essa planilha.”
* “Importe esse extrato.”
* “Remova a transação duplicada de ontem.”
* “Quanto gastei com alimentação esse mês?”
* “Crie uma planilha simples para eu controlar meus gastos.”
* “Nesse áudio, vou falar vários gastos. Registre todos.”

## 3. Decisões fechadas

As seguintes decisões estão definidas para o MVP:

```text
1. Login: somente Google.
2. Acesso ao Drive: arquivos criados pelo koin e arquivos selecionados manualmente pelo usuário.
3. Pasta principal: usuário escolhe criar uma nova pasta ou selecionar uma existente.
4. Planilha principal: usuário escolhe criar uma nova planilha ou usar uma existente.
5. Estrutura padrão da planilha: Transações, Categorias, Resumo e Histórico.
6. PostgreSQL: não armazena dados financeiros principais.
7. Histórico de mensagens: mensagens por tempo limitado e ações executadas de forma persistente.
8. MongoDB: usado para auditoria, execuções do agente e logs de processamento.
9. Auditoria: best effort, sem outbox no MVP.
10. Confirmação: somente para ações sensíveis ou em lote.
11. Ações sensíveis: remoção, edição em massa, importação, reorganização de planilhas.
12. Desfazer: ações simples recentes, como inserção de linhas.
13. Entradas: texto, áudio, upload de planilhas e PDF.
14. Formatos de planilha: Google Sheets, CSV e XLSX.
15. PDF: suporte experimental, com necessidade de revisão.
16. Áudio: deve entender comandos longos e múltiplas ações em uma única entrada.
17. Planilhas existentes: analisar estrutura, identificar colunas e pedir confirmação do mapeamento.
18. Alterações grandes em planilhas existentes: criar cópia antes ou pedir confirmação.
19. Importação de documentos: mostrar prévia e pedir confirmação.
20. Classificação: IA com regras simples aprendidas por usuário.
21. Categorias padrão: lista simples e editável.
22. Decisões financeiras: organização, leitura dos dados e sugestões simples de economia/planejamento.
23. Relatórios: somente resumos textuais na conversa.
24. Interface: chat, arquivos conectados, histórico e configurações da pasta Drive.
25. Progresso de jobs: polling por endpoint.
26. Desenvolvimento: Controller + Use Case + Repository + Adapter + Worker.
27. Organização do backend: por tipo técnico.
28. Banco PostgreSQL: mínimo + category_rules e user_preferences.
29. Arquivos enviados: enviados ao Google Drive e processados de lá.
30. Pasta padrão: Koin.
```

## 4. Escopo do MVP

O MVP do koin deverá validar o conceito principal:

> Um agente consegue organizar a vida financeira do usuário manipulando planilhas no Google Drive, a partir de comandos em linguagem natural, áudio e documentos.

O MVP deve conter:

* login com Google;
* conexão com Google Drive;
* criação ou seleção da pasta `Koin`;
* criação ou seleção de planilha financeira;
* chat com agente;
* entrada por texto;
* entrada por áudio;
* upload de CSV;
* upload de XLSX;
* upload de PDF com suporte experimental;
* leitura de Google Sheets;
* leitura de estrutura de planilhas existentes;
* criação de planilha padrão;
* inserção de registros;
* edição simples de registros;
* remoção simples de registros;
* importação de transações a partir de documentos;
* prévia antes de importações;
* confirmação antes de ações sensíveis;
* regras simples de categorização por usuário;
* histórico básico das ações executadas;
* auditoria em MongoDB;
* jobs para processamento de documentos e ações demoradas;
* resposta textual explicando o que o agente fez.

## 5. Fora do escopo do MVP

O koin não deverá implementar no MVP:

* dashboard financeiro próprio;
* gráficos avançados;
* CRUD financeiro completo no app;
* banco interno de transações;
* sistema completo de orçamento;
* sistema completo de metas;
* Open Finance;
* conexão automática com bancos;
* scraping de aplicativos bancários;
* recomendação de investimentos;
* produtos financeiros;
* aplicativo mobile nativo;
* workspace compartilhado;
* múltiplas contas financeiras internas;
* cartões internos;
* controle patrimonial;
* sistema contábil;
* ERP financeiro;
* painel administrativo financeiro.

## 6. Requisitos funcionais

### RF01 — Login com Google

O usuário deve conseguir acessar o koin usando sua conta Google.

O login com Google será obrigatório no MVP porque a aplicação depende da integração com Google Drive e Google Sheets.

### RF02 — Conectar Google Drive

O usuário deve autorizar o koin a acessar arquivos necessários no Google Drive.

O koin não deve solicitar acesso amplo desnecessário. A aplicação deve trabalhar com:

* arquivos criados pelo próprio koin;
* arquivos selecionados manualmente pelo usuário;
* pasta escolhida ou criada para uso do koin.

### RF03 — Criar ou selecionar pasta principal

No primeiro uso, o usuário deve poder:

* criar automaticamente uma pasta chamada `Koin`; ou
* selecionar uma pasta existente no Google Drive.

Essa pasta será o espaço principal de trabalho do agente.

### RF04 — Criar ou selecionar planilha financeira

O usuário deve poder:

* criar uma nova planilha financeira padrão; ou
* selecionar uma planilha existente para o agente analisar e utilizar.

### RF05 — Criar planilha padrão

Quando o usuário escolher criar uma nova planilha, o koin deverá criar uma estrutura inicial simples com as abas:

```text
Transações
Categorias
Resumo
Histórico
```

A aba `Transações` será o principal local de registro financeiro.

A aba `Categorias` conterá categorias padrão editáveis.

A aba `Resumo` poderá conter uma visão simples calculada por fórmulas ou preenchida pelo agente.

A aba `Histórico` poderá registrar alterações relevantes feitas pelo agente na própria planilha, se fizer sentido para a experiência.

### RF06 — Conversar com o agente por texto

O usuário deve poder enviar comandos financeiros em linguagem natural.

Exemplos:

```text
Gastei R$ 25 com almoço hoje.
Recebi R$ 2.000 de salário.
Remova a linha duplicada do mercado.
Quanto gastei esse mês?
Crie uma planilha para controlar meus gastos.
```

### RF07 — Enviar comandos por áudio

O usuário deve poder enviar áudios.

O sistema deverá transcrever o áudio, interpretar o conteúdo e executar as ações correspondentes.

O agente deve ser capaz de entender múltiplas ações no mesmo áudio.

Exemplo:

```text
Hoje gastei R$ 30 com almoço, R$ 12 com café, R$ 80 de gasolina e recebi R$ 500 de um serviço.
```

O agente deverá extrair as ações separadamente e registrar cada uma como linha própria ou como operação adequada na planilha.

### RF08 — Upload de documentos

O usuário deve poder enviar documentos para o agente.

Formatos suportados no MVP:

```text
CSV
XLSX
PDF experimental
```

Arquivos enviados devem ser salvos no Google Drive, dentro da pasta `Koin` ou subpasta de importações, e processados a partir de lá.

### RF09 — Ler planilhas existentes

O usuário deve poder selecionar uma planilha existente do Google Drive.

O agente deverá analisar a estrutura da planilha, identificar abas, colunas, possíveis tabelas financeiras e propor um mapeamento.

Exemplo de mapeamento:

```text
Data        → data da transação
Descrição   → descrição
Valor       → valor
Categoria   → categoria
Tipo        → receita/despesa
```

Antes de usar esse mapeamento, o agente deve solicitar confirmação do usuário.

### RF10 — Inserir linhas

O agente deve conseguir inserir linhas em uma planilha financeira.

A inserção pode acontecer a partir de:

* comando de texto;
* áudio;
* documento importado;
* correção manual solicitada pelo usuário.

### RF11 — Editar linhas

O agente deve conseguir editar linhas específicas.

Exemplo:

```text
Mude o gasto de mercado de ontem para R$ 97,50.
Corrija a categoria da compra do Uber para transporte.
```

Quando houver ambiguidade, o agente deve perguntar qual linha deve ser alterada.

### RF12 — Remover linhas

O agente deve conseguir remover linhas específicas.

Remoção de uma única linha pode ser permitida com confirmação simples ou contexto claro.

Remoção de múltiplas linhas deve sempre exigir confirmação.

### RF13 — Organizar planilhas

O agente deve conseguir ajudar o usuário a organizar uma planilha existente.

Ações possíveis:

* identificar colunas;
* sugerir estrutura;
* padronizar nomes de colunas;
* criar abas;
* mover dados para uma estrutura mais clara;
* criar uma cópia organizada da planilha;
* preservar o arquivo original em alterações grandes.

### RF14 — Importar transações

Ao receber uma planilha, CSV ou PDF, o agente deve tentar extrair transações financeiras.

O fluxo deve ser:

1. receber o arquivo;
2. salvar no Drive;
3. criar job de processamento;
4. identificar formato;
5. extrair dados;
6. interpretar colunas;
7. montar prévia;
8. solicitar confirmação;
9. inserir dados na planilha principal;
10. registrar ação executada.

### RF15 — Prévia antes de importações

Antes de inserir dados importados em massa, o koin deve exibir uma prévia.

A prévia deve mostrar:

* quantidade de registros encontrados;
* exemplos de transações;
* colunas identificadas;
* possíveis categorias;
* avisos de baixa confiança;
* duplicidades prováveis, se detectadas.

### RF16 — Confirmação para ações sensíveis

O koin deve pedir confirmação para:

* remover linhas;
* remover várias linhas;
* editar muitas células;
* importar documentos;
* reorganizar planilhas;
* alterar cabeçalhos;
* criar cópia organizada;
* substituir estrutura existente;
* qualquer ação que possa alterar muitos dados de uma vez.

### RF17 — Desfazer ações simples

O koin deve permitir desfazer ações simples recentes, principalmente:

* inserção de uma linha;
* inserção de poucas linhas;
* alteração simples em uma linha.

No MVP, desfazer importações grandes pode ficar fora do escopo, desde que o agente peça confirmação antes de importar.

### RF18 — Classificar transações

O agente deve conseguir classificar transações em categorias simples.

O sistema deverá usar IA para sugerir categorias e também salvar regras simples por usuário.

Exemplo:

```text
Uber → Transporte
iFood → Alimentação
Netflix → Assinaturas
Farmácia São Paulo → Saúde
```

Essas regras não transformam o koin em plataforma financeira. Elas servem apenas para melhorar a qualidade do agente.

### RF19 — Categorias padrão

A planilha criada pelo koin deverá possuir categorias padrão editáveis.

Exemplos:

```text
Alimentação
Transporte
Moradia
Saúde
Educação
Lazer
Assinaturas
Compras
Serviços
Renda
Outros
```

### RF20 — Responder perguntas simples

O agente deve conseguir responder perguntas simples com base nos dados da planilha.

Exemplos:

```text
Quanto gastei este mês?
Quanto gastei com alimentação?
Qual foi meu maior gasto?
Quanto entrou de receita esse mês?
Estou gastando muito com delivery?
```

Essas respostas devem ser baseadas na leitura da planilha, não em dados financeiros armazenados no banco interno.

### RF21 — Sugestões simples de organização e economia

O agente pode sugerir ações simples, como:

* reduzir uma categoria de gasto;
* separar gastos fixos e variáveis;
* criar uma aba de planejamento;
* revisar gastos recorrentes;
* estimar quanto economizar por mês para atingir uma meta simples.

O agente não deve recomendar investimentos específicos ou produtos financeiros.

### RF22 — Histórico de ações

O koin deve registrar ações executadas pelo agente.

O histórico deve permitir saber:

* quem pediu a ação;
* qual arquivo foi alterado;
* qual ação foi executada;
* quando aconteceu;
* se foi confirmada;
* se foi concluída;
* se houve erro.

### RF23 — Histórico de mensagens

O koin deve armazenar mensagens por tempo limitado.

As ações executadas devem ser mantidas de forma mais persistente.

A estratégia inicial será:

```text
Mensagens: retenção limitada.
Ações: retenção persistente enquanto a conta existir.
```

### RF24 — Configurações do Drive

A interface deve permitir:

* ver a pasta principal conectada;
* trocar a pasta principal;
* ver planilhas conectadas;
* criar nova planilha;
* selecionar planilha existente;
* abrir arquivos no Google Drive;
* desconectar a integração.

### RF25 — Progresso de jobs por polling

Tarefas demoradas serão executadas por worker.

O frontend deverá consultar periodicamente o status do job por endpoint de polling.

## 7. Requisitos obrigatórios

São obrigatórios para o MVP:

```text
- Login com Google.
- Integração com Google Drive.
- Integração com Google Sheets.
- Criação ou seleção da pasta Koin.
- Criação ou seleção de planilha financeira.
- Chat com agente.
- Entrada por texto.
- Entrada por áudio.
- Upload de CSV.
- Upload de XLSX.
- Upload experimental de PDF.
- Leitura de planilhas existentes.
- Mapeamento de estrutura de planilha.
- Inserção de linhas.
- Edição simples de linhas.
- Remoção simples de linhas.
- Confirmação para ações sensíveis.
- Prévia antes de importação em massa.
- Histórico de ações.
- PostgreSQL operacional.
- MongoDB para auditoria e rastreamento.
- Worker para tarefas demoradas.
- Logs técnicos estruturados.
- Regras simples de categorização.
- Categorias padrão.
- Respostas simples baseadas nos dados da planilha.
```

## 8. Requisitos não obrigatórios

Não são obrigatórios no MVP:

```text
- Dashboard financeiro próprio.
- Gráficos avançados.
- CRUD financeiro no app.
- Banco interno de transações.
- Open Finance.
- Integração bancária.
- Aplicativo mobile.
- Recomendações de investimento.
- Sistema completo de orçamento.
- Sistema completo de metas.
- Workspace compartilhado.
- Colaboração em tempo real.
- WebSocket.
- Server-Sent Events.
- Outbox transacional.
- Processamento avançado de PDFs complexos.
- OCR de imagens.
- Detecção perfeita de duplicidades.
- Desfazer importações grandes.
- Relatórios visuais no app.
```

## 9. Requisitos não funcionais

### RNF01 — Simplicidade

A aplicação deve ser simples e centrada no agente.

A interface não deve se transformar em sistema financeiro complexo.

### RNF02 — Segurança

Tokens do Google devem ser armazenados criptografados.

O sistema deve evitar armazenar dados financeiros sensíveis no banco interno.

### RNF03 — Privacidade

A vida financeira do usuário deve permanecer nas planilhas do Google Drive sempre que possível.

O koin não deve duplicar transações em banco próprio.

### RNF04 — Rastreabilidade

Toda ação relevante do agente deve ser rastreável.

Cada execução deve possuir identificadores como:

```text
request_id
session_id
user_id
resource_id
job_id
agent_run_id
action_id
```

### RNF05 — Tolerância a falhas de auditoria

A auditoria em MongoDB será best effort.

Se a gravação no MongoDB falhar, a operação principal não deverá ser automaticamente invalidada.

A falha deve gerar log técnico estruturado.

### RNF06 — Legibilidade

O código deve ser organizado para facilitar desenvolvimento por agentes de código.

Camadas e responsabilidades devem ser explícitas.

### RNF07 — Processamento assíncrono

Documentos, PDFs, áudios longos, planilhas grandes e importações devem rodar em worker.

### RNF08 — Validação

O agente pode interpretar, mas o backend deve validar antes de executar.

### RNF09 — Confirmação

Ações sensíveis devem exigir confirmação do usuário.

### RNF10 — Baixo acoplamento

Integrações externas devem ficar atrás de adapters.

Chamadas diretas à API do Google ou OpenAI não devem ficar espalhadas pelo código.

## 10. Arquitetura da aplicação

A arquitetura será um monólito modular simples, organizado por tipo técnico.

Visão geral:

```text
Frontend Next.js
    ↓
Backend FastAPI
    ↓
Agent Orchestrator
    ↓
Tools / Adapters
    ├── OpenAI
    ├── Google Drive
    ├── Google Sheets
    ├── File Processor
    ├── Audio Transcription
    └── Audit Logger
    ↓
PostgreSQL / MongoDB
```

## 11. Serviços da aplicação

O ambiente inicial terá os seguintes serviços:

```text
frontend
backend-api
worker
postgres
mongodb
```

### frontend

Aplicação web do usuário.

Responsável por:

* login;
* chat;
* upload de arquivos;
* gravação/envio de áudio;
* listagem de arquivos conectados;
* histórico de ações;
* configurações do Drive;
* acompanhamento de jobs por polling.

### backend-api

API principal.

Responsável por:

* autenticação;
* sessões;
* mensagens;
* orquestração do agente;
* validação;
* criação de jobs;
* integração com Google;
* resposta ao frontend.

### worker

Processa tarefas demoradas.

Responsável por:

* processar arquivos;
* processar PDFs;
* processar planilhas grandes;
* transcrever áudios longos;
* executar importações;
* gerar prévias;
* executar ações assíncronas.

### postgres

Banco operacional.

Não armazena a vida financeira do usuário.

### mongodb

Auditoria, execuções do agente e logs de processamento.

## 12. Modelo de desenvolvimento

O backend seguirá o padrão:

```text
Controller
↓
Use Case
↓
Repository / Adapter / Service
↓
Banco ou integração externa
```

Com worker separado reutilizando use cases sempre que possível.

## 13. Organização do backend

A organização será por tipo técnico, conforme decisão definida.

Estrutura sugerida:

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

### controllers

Recebem requisições HTTP.

Não devem conter regra de negócio.

### use_cases

Coordenam ações da aplicação.

Exemplos:

```text
connect_google_drive
setup_koin_folder
create_financial_sheet
send_agent_message
process_audio_input
upload_document
analyze_spreadsheet
confirm_import
insert_sheet_row
edit_sheet_row
delete_sheet_row
undo_recent_action
```

### services

Contêm lógica de aplicação reutilizável.

Exemplos:

```text
AgentService
SheetMappingService
DocumentProcessingService
CategoryRuleService
ConfirmationService
ActionHistoryService
```

### repositories

Acessam PostgreSQL.

Exemplos:

```text
UserRepository
IntegrationRepository
ResourceRepository
SessionRepository
MessageRepository
ActionRepository
JobRepository
CategoryRuleRepository
PreferenceRepository
```

### adapters

Integram com serviços externos.

Exemplos:

```text
GoogleDriveAdapter
GoogleSheetsAdapter
OpenAIAdapter
MongoAuditAdapter
AudioTranscriptionAdapter
PDFParserAdapter
SpreadsheetParserAdapter
```

### prompts

Armazenam prompts versionados.

Nenhum prompt importante deve ficar solto em controllers ou use cases.

### agent_tools

Define ferramentas controladas que o agente pode chamar.

Exemplos:

```text
create_drive_folder
create_spreadsheet
read_spreadsheet
map_sheet_columns
append_rows
update_rows
delete_rows
extract_transactions_from_file
classify_transaction
ask_confirmation
```

## 14. Papel do agente

O agente será responsável por interpretar a intenção do usuário e escolher ferramentas.

O agente não deve executar diretamente chamadas externas.

O backend disponibiliza ferramentas controladas.

Fluxo padrão:

```text
Usuário envia mensagem
↓
Backend cria ou recupera sessão
↓
AgentService prepara contexto
↓
OpenAI interpreta a intenção
↓
Agente seleciona ferramenta
↓
Backend valida parâmetros
↓
Adapter executa ação no Google Drive/Sheets
↓
Ação é registrada
↓
Agente responde ao usuário
```

## 15. Ferramentas do agente

O agente deverá ter ferramentas estruturadas.

### Ferramentas de Drive

```text
create_koin_folder
select_drive_folder
list_drive_files
save_uploaded_file_to_drive
create_file_copy
open_file_link
```

### Ferramentas de Sheets

```text
create_financial_spreadsheet
read_spreadsheet_metadata
read_sheet_rows
map_sheet_structure
append_sheet_rows
update_sheet_rows
delete_sheet_rows
create_sheet_tab
rename_sheet_tab
write_sheet_history
```

### Ferramentas de documentos

```text
parse_csv
parse_xlsx
parse_pdf_experimental
extract_financial_rows
generate_import_preview
```

### Ferramentas de categorização

```text
classify_transaction
get_user_category_rules
save_category_rule
apply_category_rules
```

### Ferramentas de segurança e confirmação

```text
create_confirmation_request
confirm_pending_action
cancel_pending_action
```

### Ferramentas de auditoria

```text
record_agent_action
record_agent_run
record_processing_log
```

## 16. Confirmação de ações

Ações simples podem ser executadas diretamente.

Exemplo:

```text
Adicione R$ 30 de almoço hoje.
```

Ações sensíveis exigem confirmação.

Exemplo:

```text
Remova todos os gastos duplicados.
Organize essa planilha inteira.
Importe esse extrato com 300 linhas.
```

Fluxo:

```text
Agente identifica ação sensível
↓
Backend cria pending action
↓
Usuário recebe resumo
↓
Usuário confirma ou cancela
↓
Backend executa ou descarta a ação
```

## 17. Casos de uso detalhados

### UC01 — Login com Google

Objetivo: permitir que o usuário acesse o koin usando sua conta Google.

Fluxo:

1. Usuário clica em entrar com Google.
2. Frontend redireciona para OAuth.
3. Google retorna código de autorização.
4. Backend valida o retorno.
5. Backend cria ou atualiza usuário.
6. Sessão é iniciada.
7. Usuário é redirecionado para a aplicação.

Resultado esperado:

```text
Usuário autenticado e pronto para configurar o Drive.
```

### UC02 — Conectar Google Drive

Objetivo: autorizar o koin a acessar arquivos necessários no Drive.

Fluxo:

1. Usuário solicita conexão com Drive.
2. Backend inicia OAuth com escopos necessários.
3. Usuário autoriza.
4. Backend recebe tokens.
5. Tokens são criptografados.
6. Integração é salva no PostgreSQL.
7. Auditoria é registrada no MongoDB.

Resultado esperado:

```text
Integração Google ativa.
```

### UC03 — Criar ou selecionar pasta Koin

Objetivo: definir a pasta principal de trabalho.

Fluxo:

1. Usuário escolhe criar pasta ou selecionar existente.
2. Se criar, backend usa Google Drive Adapter para criar `Koin`.
3. Se selecionar, backend salva o identificador da pasta.
4. Recurso é salvo em `drive_resources`.
5. Agente passa a usar essa pasta como contexto principal.

Resultado esperado:

```text
Pasta principal configurada.
```

### UC04 — Criar planilha financeira padrão

Objetivo: criar uma planilha inicial para uso do agente.

Fluxo:

1. Usuário pede para criar planilha.
2. Backend cria arquivo Google Sheets.
3. Backend cria abas padrão.
4. Backend escreve cabeçalhos básicos.
5. Backend salva recurso no PostgreSQL.
6. Agente responde com link para a planilha.

Estrutura sugerida da aba `Transações`:

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

Resultado esperado:

```text
Planilha criada no Drive e conectada ao koin.
```

### UC05 — Conectar planilha existente

Objetivo: permitir que o agente use uma planilha já existente.

Fluxo:

1. Usuário seleciona uma planilha.
2. Backend lê metadados e abas.
3. Agente analisa estrutura.
4. Agente propõe mapeamento de colunas.
5. Usuário confirma ou corrige.
6. Mapeamento é salvo em `drive_resources.metadata`.
7. Planilha passa a ser usada pelo agente.

Resultado esperado:

```text
Planilha existente mapeada e pronta para uso.
```

### UC06 — Registrar transação por texto

Objetivo: inserir um lançamento financeiro a partir de mensagem textual.

Fluxo:

1. Usuário envia mensagem.
2. Agente interpreta dados financeiros.
3. Backend valida valor, data, tipo e destino.
4. Backend aplica regra de categoria, se existir.
5. Backend insere linha na planilha.
6. Ação é registrada.
7. Agente responde ao usuário.

Exemplo de resposta:

```text
Registrei R$ 42,90 em Alimentação na sua planilha.
```

### UC07 — Registrar múltiplas ações por áudio

Objetivo: processar um áudio com vários comandos ou registros financeiros.

Fluxo:

1. Usuário envia áudio.
2. Backend salva áudio no Drive ou armazenamento temporário controlado.
3. Serviço de transcrição gera texto.
4. Agente interpreta múltiplas ações.
5. Backend separa ações em itens estruturados.
6. Se forem ações simples, executa.
7. Se houver muitas alterações, pede confirmação.
8. Cada ação executada é registrada.
9. Agente responde com resumo.

Exemplo:

```text
Registrei 4 transações:
- R$ 30 em alimentação
- R$ 12 em alimentação
- R$ 80 em transporte
- R$ 500 em receita
```

### UC08 — Upload de CSV ou XLSX

Objetivo: processar documento financeiro em formato de planilha.

Fluxo:

1. Usuário faz upload.
2. Arquivo é salvo no Google Drive.
3. Backend cria job de processamento.
4. Worker lê o arquivo.
5. Agente identifica colunas financeiras.
6. Sistema gera prévia.
7. Usuário confirma.
8. Registros são inseridos na planilha principal.

Resultado esperado:

```text
Documento processado e transações importadas após confirmação.
```

### UC09 — Upload de PDF experimental

Objetivo: tentar extrair dados financeiros de PDF.

Fluxo:

1. Usuário envia PDF.
2. Arquivo é salvo no Drive.
3. Worker processa o PDF.
4. Agente tenta identificar tabelas/transações.
5. Sistema indica nível de confiança.
6. Usuário revisa a prévia.
7. Usuário confirma ou cancela.
8. Dados confirmados são inseridos.

Observação:

```text
PDF deve ser tratado como funcionalidade experimental no MVP.
```

### UC10 — Organizar planilha existente

Objetivo: ajudar usuário a estruturar uma planilha financeira já existente.

Fluxo:

1. Usuário pede organização.
2. Agente lê estrutura da planilha.
3. Agente identifica problemas.
4. Agente propõe alterações.
5. Backend sugere criar cópia antes de grandes mudanças.
6. Usuário confirma.
7. Backend aplica alterações.
8. Ação é registrada.

Resultado esperado:

```text
Planilha organizada com segurança e confirmação.
```

### UC11 — Editar linha

Objetivo: alterar uma transação existente.

Fluxo:

1. Usuário solicita alteração.
2. Agente tenta identificar a linha.
3. Se houver ambiguidade, pergunta ao usuário.
4. Backend altera a linha.
5. Ação é registrada.
6. Agente responde.

### UC12 — Remover linha

Objetivo: remover uma transação.

Fluxo:

1. Usuário solicita remoção.
2. Agente identifica a linha.
3. Backend pede confirmação se necessário.
4. Após confirmação, linha é removida.
5. Ação é registrada.

### UC13 — Perguntar sobre dados financeiros

Objetivo: responder perguntas simples com base na planilha.

Fluxo:

1. Usuário faz pergunta.
2. Backend lê dados necessários da planilha.
3. Agente interpreta e calcula resposta simples.
4. Agente responde em linguagem natural.

Exemplo:

```text
Você gastou R$ 842,30 com alimentação neste mês.
```

### UC14 — Aprender regra de categoria

Objetivo: salvar preferência simples do usuário.

Fluxo:

1. Usuário corrige categoria.
2. Backend identifica padrão.
3. Agente pergunta se deve lembrar.
4. Usuário confirma.
5. Regra é salva em `category_rules`.

Exemplo:

```text
Sempre classificar "Uber" como Transporte.
```

### UC15 — Desfazer ação simples

Objetivo: desfazer uma inserção recente.

Fluxo:

1. Usuário pede para desfazer.
2. Backend identifica última ação reversível.
3. Backend executa operação inversa.
4. Ação é registrada.
5. Agente responde.

## 18. Modelo de banco de dados — PostgreSQL

O PostgreSQL será banco operacional.

Ele não armazenará a vida financeira completa do usuário.

### 18.1 users

Armazena usuários.

Campos principais:

```text
id
google_account_id
name
email
avatar_url
status
created_at
updated_at
last_login_at
```

### 18.2 google_integrations

Armazena integração com Google.

Campos principais:

```text
id
user_id
provider
scopes
access_token_encrypted
refresh_token_encrypted
expires_at
status
last_connected_at
last_error
created_at
updated_at
```

### 18.3 drive_resources

Armazena arquivos e pastas usados pelo koin.

Campos principais:

```text
id
user_id
integration_id
resource_type
google_file_id
google_folder_id
name
mime_type
web_url
role
status
metadata
created_at
updated_at
last_used_at
```

Tipos de recurso:

```text
koin_folder
financial_spreadsheet
uploaded_csv
uploaded_xlsx
uploaded_pdf
processed_file
spreadsheet_copy
```

Exemplo de `metadata`:

```json
{
  "sheet_tabs": ["Transações", "Categorias", "Resumo", "Histórico"],
  "primary_sheet": "Transações",
  "column_mapping": {
    "date": "Data",
    "description": "Descrição",
    "amount": "Valor",
    "category": "Categoria"
  }
}
```

### 18.4 agent_sessions

Armazena sessões de conversa.

Campos principais:

```text
id
user_id
title
status
context_summary
created_at
updated_at
last_message_at
expires_at
```

### 18.5 agent_messages

Armazena mensagens por tempo limitado.

Campos principais:

```text
id
session_id
user_id
role
content_type
content
audio_resource_id
file_resource_id
metadata
created_at
expires_at
```

Papéis:

```text
user
assistant
system
tool
```

Tipos de conteúdo:

```text
text
audio
file
confirmation
```

### 18.6 agent_actions

Armazena ações executadas ou propostas pelo agente.

Campos principais:

```text
id
user_id
session_id
resource_id
action_type
status
requires_confirmation
confirmed_at
reversible
reverted_at
input_summary
result_summary
payload
created_at
updated_at
```

Tipos de ação:

```text
create_folder
create_spreadsheet
connect_spreadsheet
append_rows
update_rows
delete_rows
import_file
organize_spreadsheet
answer_question
save_category_rule
undo_action
```

Status:

```text
pending_confirmation
confirmed
processing
completed
failed
cancelled
reverted
```

### 18.7 jobs

Armazena tarefas assíncronas.

Campos principais:

```text
id
user_id
session_id
resource_id
action_id
job_type
status
priority
payload
progress
attempts
max_attempts
error_code
error_message
created_at
scheduled_at
started_at
finished_at
locked_at
locked_by
```

Tipos de job:

```text
process_audio
process_csv
process_xlsx
process_pdf
analyze_spreadsheet
generate_import_preview
execute_import
organize_spreadsheet
```

Status:

```text
pending
processing
completed
failed
cancelled
```

### 18.8 category_rules

Armazena regras simples de categorização por usuário.

Campos principais:

```text
id
user_id
pattern
match_type
category
subcategory
confidence
source
is_active
created_at
updated_at
last_used_at
```

Tipos de match:

```text
contains
equals
regex
merchant_like
```

Exemplos:

```text
pattern: "Uber"
category: "Transporte"

pattern: "iFood"
category: "Alimentação"
```

### 18.9 user_preferences

Armazena preferências operacionais do agente.

Campos principais:

```text
id
user_id
key
value
created_at
updated_at
```

Exemplos de preferências:

```json
{
  "default_currency": "BRL",
  "default_language": "pt-BR",
  "confirm_before_bulk_changes": true,
  "default_koin_folder_resource_id": "...",
  "default_spreadsheet_resource_id": "..."
}
```

## 19. Modelo de dados — MongoDB

O MongoDB será usado para auditoria e rastreamento detalhado.

A gravação será best effort.

### 19.1 audit_events

Registra eventos importantes.

Documento base:

```json
{
  "event_id": "uuid",
  "event_type": "append_rows",
  "event_version": 1,
  "occurred_at": "2026-06-18T12:00:00Z",
  "user_id": "uuid",
  "session_id": "uuid",
  "resource_id": "uuid",
  "action_id": "uuid",
  "job_id": "uuid",
  "actor": {
    "type": "user|agent|worker|system",
    "id": "uuid"
  },
  "status": "success|failed|partial",
  "summary": "Inserted 3 rows into Transações",
  "data": {},
  "metadata": {}
}
```

### 19.2 agent_runs

Registra execuções do agente.

Campos sugeridos:

```json
{
  "agent_run_id": "uuid",
  "user_id": "uuid",
  "session_id": "uuid",
  "message_id": "uuid",
  "model": "openai-model",
  "prompt_version": "koin-agent-v1",
  "input_summary": {},
  "tool_calls": [],
  "structured_output": {},
  "tokens": {},
  "duration_ms": 0,
  "status": "success|failed",
  "error": null,
  "created_at": "2026-06-18T12:00:00Z"
}
```

### 19.3 document_processing_logs

Registra detalhes de processamento de documentos.

Campos sugeridos:

```json
{
  "processing_id": "uuid",
  "job_id": "uuid",
  "user_id": "uuid",
  "resource_id": "uuid",
  "file_type": "csv|xlsx|pdf",
  "steps": [],
  "warnings": [],
  "detected_columns": {},
  "preview_summary": {},
  "status": "success|failed|partial",
  "created_at": "2026-06-18T12:00:00Z"
}
```

## 20. Stack tecnológica

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

### Banco operacional

```text
PostgreSQL
```

### Auditoria e logs detalhados

```text
MongoDB
```

### IA

```text
OpenAI API
```

### Integrações Google

```text
Google OAuth
Google Drive API
Google Sheets API
```

### Processamento

```text
Worker Python
Fila em tabela jobs no PostgreSQL
Polling para progresso
```

### Infraestrutura inicial

```text
Docker
Docker Compose
```

## 21. Endpoints iniciais sugeridos

A especificação dos endpoints pode evoluir, mas o conjunto inicial pode ser:

```text
POST /auth/google/start
GET  /auth/google/callback
GET  /me

POST /integrations/google/connect
DELETE /integrations/google/disconnect

GET  /drive/resources
POST /drive/folder/setup
POST /drive/spreadsheets/create
POST /drive/spreadsheets/connect

POST /agent/sessions
GET  /agent/sessions
GET  /agent/sessions/{id}
POST /agent/sessions/{id}/messages

POST /agent/audio
POST /agent/files/upload

GET  /actions
GET  /actions/{id}
POST /actions/{id}/confirm
POST /actions/{id}/cancel
POST /actions/{id}/undo

GET  /jobs/{id}
```

## 22. Debug e observabilidade

Toda operação relevante deve usar identificadores de correlação.

Campos importantes:

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

Logs técnicos devem registrar:

* início de requisições;
* erros de autenticação;
* falhas de Google API;
* falhas de OpenAI;
* falhas de parsing;
* falhas de processamento;
* falhas de auditoria;
* tempo de execução;
* status final.

Dados financeiros sensíveis não devem ser registrados integralmente nos logs técnicos.

## 23. Boas práticas obrigatórias para desenvolvimento

O projeto deverá seguir estas regras:

```text
- Controllers não possuem regra de negócio.
- Use cases coordenam fluxos.
- Repositories acessam PostgreSQL.
- Adapters acessam APIs externas.
- Prompts são versionados.
- Ferramentas do agente são estruturadas.
- Nenhuma ação crítica é executada sem validação.
- Ações sensíveis exigem confirmação.
- MongoDB não é fonte de verdade operacional.
- PostgreSQL não armazena a vida financeira completa do usuário.
- Jobs demorados rodam no worker.
- Worker reutiliza use cases quando possível.
- Tokens Google são criptografados.
- Logs financeiros devem ser minimizados.
- Código deve ser legível para agentes de código.
```

## 24. Diretrizes para agentes de código

Os agentes de código que desenvolverem o koin devem seguir estas diretrizes:

```text
1. Ler a documentação antes de alterar código.
2. Não transformar o koin em app financeiro tradicional.
3. Não criar tabelas internas de transações, orçamentos ou metas.
4. Manter o Google Drive/Sheets como centro da organização financeira.
5. Não adicionar dashboards financeiros próprios no MVP.
6. Não espalhar chamadas diretas ao Google, OpenAI ou MongoDB.
7. Criar adapters para integrações externas.
8. Manter prompts centralizados e versionados.
9. Usar schemas Pydantic para entradas e saídas estruturadas.
10. Criar testes para parsers e ferramentas do agente.
11. Criar fixtures de CSV, XLSX e PDFs simples.
12. Tratar PDF como experimental.
13. Preservar confirmação antes de alterações sensíveis.
14. Atualizar documentação quando alterar fluxo importante.
```

## 25. Critérios de sucesso do MVP

O MVP será considerado bem-sucedido se permitir que um usuário:

```text
1. Entre com Google.
2. Conecte o Drive.
3. Crie ou selecione uma pasta Koin.
4. Crie ou conecte uma planilha financeira.
5. Registre gastos por texto.
6. Registre múltiplas ações por áudio.
7. Faça upload de CSV ou XLSX.
8. Receba uma prévia antes de importar.
9. Confirme a importação.
10. Veja os dados organizados no Google Sheets.
11. Peça ao agente respostas simples sobre a planilha.
12. Veja histórico básico do que foi feito.
```

## 26. Definição final

O koin será construído como um agente de finanças pessoais, não como uma plataforma financeira tradicional.

A aplicação terá uma interface web simples, centrada em conversa, com suporte a texto, áudio e documentos.

O Google Drive será o espaço de trabalho do usuário.

O Google Sheets será o local principal onde os dados financeiros serão organizados.

O PostgreSQL armazenará apenas dados operacionais.

O MongoDB armazenará auditoria, execuções do agente e logs detalhados de processamento.

A IA interpretará comandos e documentos.

O backend validará, executará e registrará ações.

A regra central do projeto é:

> O koin não gerencia finanças dentro da aplicação. O koin ajuda o usuário a organizar suas finanças nas próprias planilhas do Google Drive.
