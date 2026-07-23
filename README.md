<!-- ====================================================== -->
<!-- HERO -->
<!-- ====================================================== -->

<h1 align="center">
    🛠️ Help Desk API
</h1>

<p align="center">
    Projeto de uma API REST para gerenciamento de chamados internos desenvolvida com FastAPI.
</p>

<div aling="center" style="display: flex; flex-flow: row wrap; gap: 5px; justify-content: center;">
<img src="https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python">
<img src="https://img.shields.io/badge/FastAPI-0.139-009688?style=for-the-badge&logo=fastapi">
<img src="https://img.shields.io/badge/SQLAlchemy-2.0-red?style=for-the-badge&logo=sqlalchemy">
<img src="https://img.shields.io/badge/PostgreSQL-17-336791?style=for-the-badge&logo=postgresql">
<img src="https://img.shields.io/badge/Docker-Pronto-2496ED?style=for-the-badge&logo=docker">
<img src="https://img.shields.io/badge/Alembic-Migrations-orange?style=for-the-badge">
<img src="https://img.shields.io/badge/Poetry-Gerenciador%20de%20Dependências-60A5FA?style=for-the-badge&logo=poetry">
<img src="https://img.shields.io/badge/Licença-MIT-success?style=for-the-badge">
</div>

---

<h2>📖 Sobre o Projeto</h2>

<p align="justify">

O <strong>Help Desk API</strong> é uma API REST para gerenciamento de chamados de suporte técnico em ambientes corporativos.

O projeto permite que colaboradores abram chamados de suporte enquanto técnicos podem assumir, acompanhar e concluir cada atendimento.

Meu principal objetivo com este projeto foi praticar conceitos fundamentais do desenvolvimento backend, aplicando arquitetura em camadas, separação de responsabilidades, autenticação com JWT, versionamento do banco de dados com Alembic, containerização com Docker e deploy da aplicação utilizando Render.

</p>

<h2>📑 Sumário</h2>

<ul>
    <li><a href="#funcionalidades">✨ Funcionalidades</a></li>
    <li><a href="#tecnologias-utilizadas">🚀 Tecnologias Utilizadas</a></li>
    <li>
        <a href="#regras-de-negocio">📋 Regras de Negócio</a>
        <ul>
            <li><a href="#usuarios">👤 Usuários</a></li>
            <li><a href="#abertura-de-chamados">🎫 Abertura de Chamados</a></li>
            <li><a href="#atendimento">🛠 Atendimento</a></li>
            <li><a href="#reabertura-de-chamados">🔄 Reabertura de Chamados</a></li>
            <li><a href="#exclusao-de-chamados">🗑 Exclusão de Chamados</a></li>
            <li><a href="#historico">📄 Histórico</a></li>
            <li><a href="#controle-de-acesso">🔐 Controle de Acesso</a></li>
            <li><a href="#dashboard-administrativa">📊 Dashboard Administrativa</a></li>
        </ul>
    </li>
    <li><a href="#estrutura-do-projeto">📁 Estrutura do Projeto</a></li>
    <li>
    <a href="#estrutura-do-banco-de-dados">🗄️ Estrutura do Banco de Dados</a>
    <ul>
        <li><a href="#user">👤 User</a></li>
        <li><a href="#Ticket">🎫 Ticket</a></li>
        <li><a href="#Ticket-History">📝 Ticket History</a></li>
        <li><a href="#relacionamentos">🔗 Relacionamentos</a></li>
    </ul>
</li>
    <li><a href="#executando-o-projeto">🚀 Executando o Projeto</a></li>
    <li><a href="#variaveis-de-ambiente">⚙️ Variáveis de Ambiente</a></li>
    <li><a href="#testes">👁️‍🗨️ Testes</a></li>
    <li><a href="#deploy">🚀 Deploy</a></li>
    <li><a href="#integracao-continua">⚙️ Integracão Continua</a></li>
    <li><a href="#licenca">🪪 Licença</a></li>
</ul>

<hr>

<h2 id="funcionalidades">✨ Funcionalidades</h2>

<ul>

<li>🔐 Autenticação utilizando JWT</li>

<li>👤 Cadastro e gerenciamento de usuários</li>

<li>🎫 Criação e acompanhamento de chamados</li>

<li>⚡ Definição de prioridades</li>

<li>👨‍🔧 Atribuição de chamados para técnicos</li>

<li>📋 Histórico de alterações dos chamados</li>

<li>🛡️ Controle de acesso baseado em perfis de usuário</li>

<li>🗄️ Versionamento do banco de dados com Alembic</li>

<li>🐳 Execução da aplicação utilizando Docker</li>

<li>☁️ Preparado para deploy no Render</li>

</ul>

---

<h2 id="tecnologias-utilizadas">🚀 Tecnologias Utilizadas</h2>

<table>

<tr>
<th>Tecnologia</th>
<th>Finalidade</th>
</tr>

<tr>
<td><strong>Python 3.14</strong></td>
<td>Linguagem principal da aplicação</td>
</tr>

<tr>
<td><strong>FastAPI</strong></td>
<td>Desenvolvimento da API REST</td>
</tr>

<tr>
<td><strong>SQLAlchemy 2.0</strong></td>
<td>Mapeamento objeto-relacional (ORM)</td>
</tr>

<tr>
<td><strong>PostgreSQL</strong></td>
<td>Banco de dados relacional</td>
</tr>

<tr>
<td><strong>Alembic</strong></td>
<td>Controle de migrations do banco</td>
</tr>

<tr>
<td><strong>Poetry</strong></td>
<td>Gerenciamento de dependências</td>
</tr>

<tr>
<td><strong>Docker</strong></td>
<td>Containerização da aplicação</td>
</tr>

<tr>
<td><strong>Pytest</strong></td>
<td>Testes automatizados</td>
</tr>

<tr>
<td><strong>JWT</strong></td>
<td>Autenticação e autorização</td>
</tr>

<tr>
<td><strong>Render</strong></td>
<td>Hospedagem da aplicação</td>
</tr>

</table>

---

<h2 id="regras-de-negocio">📋 Regras de Negócio</h2>

<p>

Antes de iniciar o desenvolvimento, defini algumas regras de negócio para representar o fluxo de um sistema de Help Desk. Elas determinam quem pode executar cada ação e em quais situações ela é permitida.

</p>

<h3 id="usuarios">👤 Usuários</h3>

<ul>
  <li>Todo usuário possui um perfil (<code>role</code>) que define suas permissões na aplicação.</li>
  <li>Os perfis disponíveis são <strong>Employee</strong>, <strong>Technician</strong> e <strong>Admin</strong>.</li>
  <li>O cadastro público permite apenas usuários dos tipos <strong>Employee</strong> e <strong>Technician</strong>.</li>
  <li>Somente administradores podem criar novos usuários com perfil <strong>Admin</strong>.</li>
</ul>

<h3 id="abertura-de-chamados">🎫 Abertura de Chamados</h3>

<ul>
  <li>Chamados podem ser criados exclusivamente por usuários <code>ROLE:</code><strong>Employee</strong>.</li>
  <li>Todo chamado é criado sem um técnico responsável.</li>
  <li>O campo <code>responsible_id</code> permanece <code>null</code> até que algum técnico assuma o atendimento.</li>
</ul>

<h3 id="atendimento">🛠 Atendimento</h3>

<ul>
  <li>Somente usuários <strong>Technician</strong> podem assumir chamados.</li>
  <li>Ao assumir um chamado, o técnico passa a ser o responsável pelo atendimento.</li>
  <li>Enquanto o chamado estiver atribuído, ele deixa de aparecer como disponível para outros técnicos.</li>
  <li>O técnico pode concluir o atendimento ou liberar o chamado para que outro profissional o assuma.</li>
</ul>

<h3 id="reabertura-de-chamados">🔄 Reabertura de Chamados</h3>

<ul>
  <li>Depois que um chamado é concluído, o autor pode reabri-lo caso o problema continue ou volte a acontecer.</li>
  <li>Após a reabertura, o chamado retorna para a fila de atendimento.</li>
</ul>

<h3 id="exclusao-de-chamados">🗑 Exclusão de Chamados</h3>

<ul>
  <li>O autor pode excluir um chamado somente antes de ele ser assumido por um técnico.</li>
  <li>A exclusão é lógica (<em>soft delete</em>), alterando apenas o status do chamado para <code>deleted</code>.</li>
</ul>

<h3 id="historico">📄 Histórico</h3>

<ul>
  <li>Todas as ações realizadas em um chamado são registradas automaticamente.</li>
  <li>O histórico inclui eventos como:</li>
  <ul>
    <li>Criação do chamado.</li>
    <li>Assumir atendimento.</li>
    <li>Remover responsabilidade.</li>
    <li>Conclusão.</li>
    <li>Reabertura.</li>
    <li>Exclusão.</li>
  </ul>
  <li>Cada registro informa quem realizou a ação, quando ela aconteceu e, quando necessário, quais informações foram alteradas.</li>
</ul>

<h3 id="controle-de-acesso">🔐 Controle de Acesso</h3>

<ul>
  <li><strong>Employee</strong> pode criar, consultar e acompanhar os próprios chamados.</li>
  <li><strong>Technician</strong> pode visualizar chamados disponíveis, assumir atendimentos, concluir chamados e liberar atendimentos sob sua responsabilidade.</li>
  <li><strong>Admin</strong> possui acesso aos recursos administrativos da aplicação, incluindo o histórico completo de alterações e a dashboard.</li>
</ul>

<h3 id="dashboard-administrativa">📊 Dashboard Administrativa</h3>

<ul>
  <li>A dashboard é exclusiva para usuários <strong>Admin</strong>.</li>
  <li>Nela são apresentados indicadores gerais, como quantidade de chamados criados, concluídos e outras métricas da aplicação.</li>
</ul>

<p align="justify">

Optei por organizar a aplicação utilizando uma arquitetura em camadas, separando as responsabilidades entre a interface HTTP, as regras de negócio e o acesso aos dados. Essa estrutura deixa o código mais organizado, facilita a manutenção e torna a criação de testes mais simples.

</p>

<pre>
                Cliente
                   │
            Requisição HTTP
                   │
              FastAPI Router
                   │
              Service Layer
                   │
            SQLAlchemy (ORM)
                   │
               PostgreSQL
</pre>

<h2 id="estrutura-do-projeto">📁 Estrutura do Projeto</h2>

<pre>
help-desk-api/
│
├── Dockerfile
├── docker-compose.yml
├── .env
├── LICENSE
├── README.md
│
└── help_desk_api/
    ├── pyproject.toml
    ├── poetry.lock
    ├── alembic.ini
    │
    ├── alembic/
    │   ├── env.py
    │   └── versions/
    │
    ├── src/
    │   └── help_desk_api/
    │       ├── main.py
    │       │
    │       ├── config/
    │       │   └── settings.py
    │       │
    │       ├── db/
    │       │   ├── base.py
    │       │   ├── session.py
    │       │   ├── enum/
    │       │   └── models/
    │       │
    │       ├── routers/
    │       │
    │       ├── services/
    │       │
    │       ├── schema/
    │       │
    │       ├── security/
    │       │
    │       └── exceptions/
    │
    └── tests/
        ├── conftest.py
        ├── test_user.py
        ├── test_employee_ticket.py
        └── test_technician_ticket.py
</pre>

<h2 id="estrutura-do-banco-de-dados">🗄️ Estrutura do Banco de Dados</h2>

<p>

Modelei o banco de dados utilizando <strong>SQLite</strong> no inicio (no render migrei para postgresql), separando as informações em três entidades principais: usuários, chamados e histórico. Essa estrutura mantém os dados organizados e permite acompanhar todas as ações realizadas durante o atendimento de um chamado.

</p>

<h3 id="user">👤 User</h3>

<p>

Armazena os usuários da aplicação e o perfil de acesso de cada um.

</p>

<ul>
    <li><strong>id</strong> — Identificador único. [pk]</li>
    <li><strong>name</strong> — Nome do usuário.</li>
    <li><strong>email</strong> — E-mail utilizado para autenticação.</li>
    <li><strong>password</strong> — Senha armazenada de forma criptografada.</li>
    <li><strong>role</strong> — Perfil do usuário (<strong>Employee</strong>, <strong>Technician</strong> ou <strong>Admin</strong>).</li>
</ul>

<h3 id="Ticket">🎫 Ticket</h3>

<p>

Representa um chamado de suporte criado por um colaborador.

</p>

<ul>
    <li><strong>id</strong> — Identificador único. [pk]</li>
    <li><strong>title</strong> — Título do chamado.</li>
    <li><strong>description</strong> — Descrição do problema.</li>
    <li><strong>creator_id</strong> — Usuário que abriu o chamado. [fk]</li>
    <li><strong>responsible_id</strong> — Técnico responsável pelo atendimento. [fk]</li>
    <li><strong>priority</strong> — Prioridade definida na abertura.</li>
    <li><strong>status</strong> — Situação atual do chamado.</li>
    <li><strong>created_at</strong> — Data de criação.</li>
</ul>

<h3 id="Ticket-History">📝 Ticket History</h3>

<p>

Registra todas as ações realizadas em um chamado.

</p>

<ul>
    <li><strong>id</strong> — Identificador único. [pk]</li>
    <li><strong>ticket_id</strong> — Chamado relacionado. [fk]</li>
    <li><strong>user_id</strong> — Usuário que realizou a ação. [fk]</li>
    <li><strong>action</strong> — Operação executada.</li>
    <li><strong>old_value</strong> — Valor anterior, quando existir.</li>
    <li><strong>new_value</strong> — Novo valor registrado.</li>
    <li><strong>performed_at</strong> — Data e horário da ação.</li>
</ul>

<h3 id="relacionamentos">🔗 Relacionamentos</h3>

<p>

Os relacionamentos entre as entidades foram definidos para representar o fluxo completo de atendimento dos chamados.

</p>

<pre><code>
User (1) ──────────────── (*) Ticket
      │                     (creator_id)

User (1) ──────────────── (*) Ticket
      │                  (responsible_id)

Ticket (1) ────────────── (*) TicketHistory

User (1) ──────────────── (*) TicketHistory
</code></pre>

<p>

Com essa modelagem é possível identificar quem criou um chamado, qual técnico ficou responsável pelo atendimento e consultar todo o histórico de alterações registradas.

</p>

<p align="justify">

A estrutura foi organizada seguindo uma arquitetura modular, facilitando a separação de responsabilidades e tornando a aplicação mais escalável e de fácil manutenção.

</p>

---

<h2 id="executando-o-projeto">🚀 Executando o Projeto</h2>

<h3>Pré-requisitos</h3>

<ul>

<li>Python 3.14+</li>

<li>Poetry</li>

<li>Docker e Docker Compose</li>

</ul>

<h3>1. Clone o repositório</h3>

```bash
git clone https://github.com/0arKes/help-desk.git

cd help-desk-api
```

<h3>2. Configure as variáveis de ambiente</h3>

<p>

Crie um arquivo <strong>.env</strong> na raiz do projeto contendo as variáveis necessárias.

</p>

<h3>3. Execute utilizando Docker</h3>

```bash
docker compose up --build
```

<p>

Durante a inicialização, o Alembic executa automaticamente as migrations do banco de dados e inicia a aplicação.

</p>

<h3>4. Acesse a documentação</h3>

```text
http://localhost:8000/docs
```

---

<h2 id="variaveis-de-ambiente">⚙️ Variáveis de Ambiente</h2>

<p>

Utilizei variáveis de ambiente para manter informações sensíveis e configurações da aplicação fora do código-fonte. Isso facilita a configuração em diferentes ambientes e evita expor dados como credenciais e chaves de autenticação.

</p>

<table>

<tr>
<th>Variável</th>
<th>Descrição</th>
</tr>

<tr>
<td><code>DATABASE_URL</code></td>
<td>URL de conexão com o PostgreSQL.</td>
</tr>

<tr>
<td><code>JWT_KEY</code></td>
<td>Chave utilizada para assinar os tokens JWT.</td>
</tr>

<tr>
<td><code>JWT_ALGORITHM</code></td>
<td>Algoritmo utilizado na geração dos tokens.</td>
</tr>

<tr>
<td><code>JWT_EXP</code></td>
<td>Tempo de expiração do token (em minutos).</td>
</tr>

</table>

<p>

O carregamento dessas configurações é feito com <strong>Pydantic Settings</strong>, permitindo utilizar configurações diferentes para desenvolvimento, testes e produção sem precisar alterar o código da aplicação.

</p>

<h2 id="testes">👁️‍🗨️ Testes</h2>

<p>

Também adicionei testes automatizados utilizando <strong>Pytest</strong> para validar os principais fluxos da aplicação, como autenticação, cadastro de usuários e algumas regras de negócio.

</p>

<ul>
    <li>Pytest</li>
    <li>Pytest Asyncio</li>
    <li>Pytest Cov</li>
</ul>

<p>

Para executar os testes:

</p>

[taskpy]
<pre><code>poetry run task test
</code></pre>

<hr>

<h2 id="deploy">🚀 Deploy</h2>
<p>Para acessar o deploy do render, basta clicar no <a href="https://help-desk-lln7.onrender.com/docs">Link</a>.</p>

<h2 id="integracao-continua">⚙️ Integração Contínua</h2>

<p>

Configurei uma pipeline de <strong>GitHub Actions</strong> para executar automaticamente os testes sempre que um <strong>push</strong> ou <strong>pull request</strong> é enviado ao repositório. Dessa forma, consigo verificar rapidamente se uma alteração introduziu algum problema antes de ela ser integrada ao projeto.

</p>

<p>

Durante a execução, a pipeline prepara o ambiente Python, instala as dependências com <strong>Poetry</strong>, carrega as variáveis de ambiente configuradas no GitHub e executa toda a suíte de testes utilizando <strong>Pytest</strong>. Como os testes utilizam um banco SQLite em memória, não foi necessário configurar containers nem executar migrations, deixando a execução mais rápida.

</p>

<h2 id="licenca">🪪 Licença</h2>

<p>

Este projeto está licenciado sob a licença <strong>MIT</strong>.

</p>

