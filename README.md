# 🧠 empatIA

> *"empatia + IA — potencializando o olhar humano com tecnologia"*

Sistema inteligente de monitoramento emocional pervasivo para o ambiente escolar, desenvolvido por estudantes do **CETI Liceu Parnaibano** (Parnaíba — Piauí), sob orientação do Prof. Marcos José Souza do Nascimento.

---

## Sumário

- [O Problema](#-o-problema)
- [A Solução](#-a-solução)
- [Público-Alvo](#-público-alvo)
- [Arquitetura Técnica](#️-arquitetura-técnica)
- [Modelos de Dados](#️-modelos-de-dados)
- [Endpoints — Especificação](#-endpoints--especificação)
- [Casos de Uso](#-casos-de-uso)
- [Funcionalidades Principais](#-funcionalidades-principais)
- [Roadmap](#️-roadmap)
- [Como Rodar (Dev)](#-como-rodar-desenvolvimento)
- [Ética e Privacidade](#-ética-e-privacidade)
- [Modelo de Negócio](#-modelo-de-negócio)
- [Contexto Institucional](#-contexto-institucional)
- [Referências](#-referências)

---

## 📌 O Problema

A saúde mental de estudantes brasileiros vive uma crise silenciosa e crescente. Dados da **Pesquisa Nacional de Saúde do Escolar (PeNSe 2024)** revelam que:

- **3 em cada 10** estudantes entre 13 e 17 anos sentem tristeza de forma contínua
- **18,5%** acreditam que a vida não vale a pena ser vivida
- **Menos da metade** frequenta escolas que oferecem algum tipo de suporte emocional

O cenário foi agravado no período pós-pandemia, quando o isolamento social aprofundou vulnerabilidades emocionais de crianças e adolescentes. Comportamentos como abandono de convivências sociais, desmotivação e crises de ansiedade impactam diretamente o rendimento acadêmico e a permanência dos alunos na escola.

O maior problema estrutural é que **as escolas só reagem em momentos de crise** — muitas vezes já com episódios graves de automutilação, indisciplina ou violência. Faltam ferramentas contínuas e preventivas integradas à rotina escolar para identificar precocemente os sinais de desequilíbrio emocional.

---

## 💡 A Solução

O **empatIA** integra-se à infraestrutura de câmeras de segurança já existente nas escolas e processa as imagens em tempo real com bibliotecas de IA especializadas em visão computacional. A partir dessa análise, o sistema:

- **Identifica** os estudantes por reconhecimento facial
- **Reconhece** expressões emocionais e posturas corporais
- **Detecta** padrões de isolamento social
- **Alerta** o núcleo gestor (diretores, coordenadores e orientadores) de forma imediata

Tudo isso de forma **contínua, não intrusiva e sem exigir qualquer ação por parte dos alunos**.

---

## 👥 Público-Alvo

| Perfil | Descrição |
|---|---|
| **Usuários monitorados** | Crianças e jovens em idade escolar matriculados em escolas públicas e privadas |
| **Usuários operadores** | Diretores, coordenadores pedagógicos e orientadores educacionais — recebem alertas e conduzem ações de acolhimento |

---

## 🏗️ Arquitetura Técnica

### Visão geral do fluxo

```
Câmeras existentes na escola (DVR)
        │
        ▼
   API de processamento (visão computacional)
   ┌────────────────────────────────────────────┐
   │  YOLO        → detecção de pessoas e       │
   │                comportamentos              │
   │  InsightFace → reconhecimento facial       │
   │  DBSCAN      → análise de expressões       │
   │                e padrões de isolamento     │
   └────────────────────────────────────────────┘
        │
        ▼
      Redis (mensageria em tempo real)
        │
        ▼
   Backend Django + Django Ninja
        │
   ┌────┴────────────────────────┐
   ▼                             ▼
Painel Web (navegador)      WhatsApp (WAHA)
alertas + relatórios        notificações em tempo real
```

### Organização do backend

O backend está organizado em camadas dentro de cada `app` Django:

| Camada | Responsabilidade |
|---|---|
| `api/` | Rotas e schemas (Django Ninja) |
| `application/` | DTOs e casos de uso (use cases) |
| `domain/` | Entidades, value objects, regras e exceções |
| `infrastructure/` | Modelos Django e repositórios |

Apps presentes: `Accounts`, `Schools`, `Users`, `Classroom`

### Stack completa

| Camada | Tecnologia |
|---|---|
| Detecção de pessoas | YOLO |
| Reconhecimento facial | InsightFace |
| Análise comportamental | DBSCAN |
| Mensageria / cache | Redis |
| Backend | Python · Django · Django Ninja |
| Banco de dados | SQLite (dev) · PostgreSQL (produção) |
| Frontend | JavaScript |
| Notificações push | WAHA (WhatsApp) |

---

## 🗄️ Modelos de Dados

### `Accounts.User`

| Campo | Tipo | Observação |
|---|---|---|
| `id` | UUID | PK |
| `name` | string | — |
| `email` | string | unique |
| `password` | string | hash (max 12) |
| `rule` | enum | perfil do usuário |
| `active` | bool | — |
| `created_at` | datetime | — |
| `deleted_at` | datetime | soft delete |
| `is_staff` | bool | — |
| `is_superuser` | bool | — |

### `Accounts.Token`

| Campo | Tipo | Observação |
|---|---|---|
| `id` | UUID | PK |
| `hash_token` | string | — |
| `user` | FK → Accounts.User | nullable |
| `expire_at` | datetime | — |
| `created_at` | datetime | — |
| `revoked` | bool | — |

### `Schools.School`

| Campo | Tipo | Observação |
|---|---|---|
| `id` | UUID | PK |
| `name` | string | — |
| `cnpj` | string | validado via value object |
| `logo` | file | upload, opcional |
| `gre` | string | Gerência Regional de Educação |
| `created_at` | datetime | — |
| `deleted_at` | datetime | soft delete |

### `Classroom.Classroom`

| Campo | Tipo | Observação |
|---|---|---|
| `id` | UUID | PK |
| `course` | string | — |
| `school` | FK → Schools.School | — |
| `created_at` | datetime | — |
| `deleted_at` | datetime | soft delete |

### `Users.Student`

| Campo | Tipo | Observação |
|---|---|---|
| `id` | UUID | PK |
| `user` | OneToOne → Accounts.User | — |
| `classroom` | FK → Classroom.Classroom | — |
| `date_birth` | date | — |
| `photo` | file | — |
| `vector_facial` | JSON | embeddings gerados pelo InsightFace |

### `Users.Coordinator`

| Campo | Tipo | Observação |
|---|---|---|
| `id` | UUID | PK |
| `user` | OneToOne → Accounts.User | — |
| `school` | FK → Schools.School | — |

### `Users.Director`

| Campo | Tipo | Observação |
|---|---|---|
| `id` | UUID | PK |
| `user` | OneToOne → Accounts.User | — |
| `school` | OneToOne → Schools.School | nullable |

---


## 📋 Casos de Uso

### UC01 — Cadastro do Usuário
**Escopo:** Accounts  
**Ator Primário:** Usuário (pessoa que deseja se registrar)  
**Pré-condição:** Não deve existir conta ativa com o mesmo e-mail

**Cenário principal de sucesso:**
1. O sistema valida se o e-mail já está cadastrado
2. O sistema valida o formato do e-mail
3. O sistema valida se a senha foi informada e se é forte
4. O sistema persiste `Accounts.User` e retorna `201`

**Garantia de sucesso:** Usuário cadastrado e dados de conta retornados (sem senha)

**Extensões:**
- `1a` — E-mail já cadastrado → `409 Conflict`
- `3b` — Senha fraca ou ausente → `400 Bad Request`

---

### UC02 — Login do Usuário
**Escopo:** Accounts  
**Ator Primário:** Usuário  
**Pré-condição:** Conta ativa com e-mail e senha válidos

**Cenário principal de sucesso:**
1. O sistema autentica as credenciais
2. O sistema emite `Token` de acesso e refresh
3. O sistema retorna `201` com `TokenOut`

**Garantia de sucesso:** Usuário recebe tokens para chamadas autenticadas subsequentes

**Extensões:**
- `1a` — Credenciais inválidas → `401 Unauthorized`
- `1b` — Conta desativada → `403 Forbidden`

---

### UC03 — Cadastro do Estudante
**Escopo:** Users.Student  
**Ator Primário:** Coordenador / Diretor  
**Pré-condição:** Turma (`Classroom`) existente no sistema

**Cenário principal de sucesso:**
1. O sistema recebe dados do formulário e foto
2. O sistema valida campos obrigatórios (nome, e-mail, classroom, data de nascimento)
3. O sistema persiste `Users.Student` vinculado a `Accounts.User`
4. O sistema armazena metadados da foto e retorna `201` com `StudentOut`

**Garantia de sucesso:** Estudante cadastrado e vinculado a uma conta e turma

**Extensões:**
- `1a` — Foto inválida ou acima do tamanho permitido → `400 Bad Request`
- `2b` — Classroom inexistente → `400 Bad Request`

---

### UC04 — Cadastro da Escola
**Escopo:** Schools.School  
**Ator Primário:** Diretor / Administrador  
**Pré-condição:** Nenhuma

**Cenário principal de sucesso:**
1. O sistema recebe dados da escola (nome, CNPJ, GRE) e logo
2. O sistema valida o CNPJ via `value_objects`
3. O sistema persiste `Schools.School` e retorna `201` com `SchoolOut`

**Garantia de sucesso:** Escola cadastrada e disponível para associar diretores e coordenadores

**Extensões:**
- `2a` — CNPJ inválido → `400 Bad Request`
- `2b` — Escola já cadastrada → `409 Conflict`

---

### UC05 — Consulta do Usuário por ID
**Escopo:** Accounts
**Ator Primário:** Usuário autenticado
**Pré-condição:** Conta do usuário existe e está ativa

**Cenário principal de sucesso:**
1. O sistema busca `Accounts.User` por ID
2. O sistema valida que o usuário existe
3. O sistema retorna `UserOut` com os dados do usuário

**Garantia de sucesso:** Dados do usuário retornados para exibição de perfil

**Extensões:**
- `1a` — Usuário não encontrado → `404 Not Found`

---

### UC06 — Consulta do Usuário por E-mail
**Escopo:** Accounts
**Ator Primário:** Usuário autenticado / Administrador
**Pré-condição:** E-mail informado corresponde a uma conta cadastrada

**Cenário principal de sucesso:**
1. O sistema busca `Accounts.User` por e-mail
2. O sistema valida que o usuário existe
3. O sistema retorna `UserOut` com os dados do usuário

**Garantia de sucesso:** Usuário localizado por e-mail para verificação ou recuperação

**Extensões:**
- `1a` — Usuário não encontrado → `404 Not Found`

---

### UC07 — Listagem de Usuários por Regra
**Escopo:** Accounts
**Ator Primário:** Administrador
**Pré-condição:** Regra válida (`STUDENT`, `COORDINATOR`, `DIRECTOR`, etc.)

**Cenário principal de sucesso:**
1. O sistema consulta `Accounts.User` pela regra definida
2. O sistema retorna a lista de usuários correspondentes

**Garantia de sucesso:** Lista de usuários filtrada por perfil retornada

**Extensões:**
- `1a` — Nenhum usuário encontrado → lista vazia retornada

---

### UC08 — Atualização do Usuário
**Escopo:** Accounts
**Ator Primário:** Usuário ou Administrador
**Pré-condição:** Conta ativa existente no sistema

**Cenário principal de sucesso:**
1. O sistema busca `Accounts.User` por ID
2. O sistema aplica alterações válidas nos campos informados
3. O sistema salva a conta atualizada e retorna `UserOut`

**Garantia de sucesso:** Dados do usuário alterados e persistidos

**Extensões:**
- `1a` — Usuário não encontrado → `404 Not Found`

---

### UC09 — Desativação do Usuário
**Escopo:** Accounts
**Ator Primário:** Administrador
**Pré-condição:** Conta existente no sistema

**Cenário principal de sucesso:**
1. O sistema busca `Accounts.User` por ID
2. O sistema marca a conta como inativa
3. O sistema salva a alteração e retorna `UserOut`

**Garantia de sucesso:** Usuário desativado e não pode mais autenticar

**Extensões:**
- `1a` — Usuário não encontrado → `404 Not Found`

---

### UC10 — Consulta da Escola por ID
**Escopo:** Schools
**Ator Primário:** Diretor / Administrador
**Pré-condição:** Escola cadastrada no sistema

**Cenário principal de sucesso:**
1. O sistema busca `Schools.School` por ID
2. O sistema valida que a escola existe
3. O sistema retorna `SchoolOut` com os dados da escola

**Garantia de sucesso:** Dados da escola retornados corretamente

**Extensões:**
- `1a` — Escola não encontrada → `404 Not Found`

---

### UC11 — Consulta da Escola por CNPJ
**Escopo:** Schools
**Ator Primário:** Diretor / Administrador
**Pré-condição:** CNPJ válido informado

**Cenário principal de sucesso:**
1. O sistema busca `Schools.School` por CNPJ
2. O sistema valida que a escola existe
3. O sistema retorna `SchoolOut` com os dados da escola

**Garantia de sucesso:** Escola localizada por CNPJ

**Extensões:**
- `1a` — Escola não encontrada → `404 Not Found`

---

### UC12 — Atualização da Escola
**Escopo:** Schools
**Ator Primário:** Diretor / Administrador
**Pré-condição:** Escola existente no sistema

**Cenário principal de sucesso:**
1. O sistema busca `Schools.School` por ID
2. O sistema aplica alterações válidas nos campos informados
3. O sistema salva a escola atualizada e retorna `SchoolOut`

**Garantia de sucesso:** Dados da escola atualizados e persistidos

**Extensões:**
- `1a` — Escola não encontrada → `404 Not Found`

---

### UC13 — Desativação da Escola
**Escopo:** Schools
**Ator Primário:** Diretor / Administrador
**Pré-condição:** Escola existente no sistema

**Cenário principal de sucesso:**
1. O sistema busca `Schools.School` por ID
2. O sistema marca a escola como inativa
3. O sistema salva a alteração e retorna `SchoolOut`

**Garantia de sucesso:** Escola desativada e não participa de novos cadastros

**Extensões:**
- `1a` — Escola não encontrada → `404 Not Found`

---

### UC14 — Cadastro da Turma
**Escopo:** Classroom
**Ator Primário:** Diretor / Administrador
**Pré-condição:** Escola existente e ativa

**Cenário principal de sucesso:**
1. O sistema valida se o curso já está cadastrado
2. O sistema valida a existência e o estado da escola vinculada
3. O sistema persiste `Classroom` e retorna `201`

**Garantia de sucesso:** Turma cadastrada e associada à escola

**Extensões:**
- `1a` — Curso já existente → `409 Conflict`
- `2a` — Escola não encontrada ou inativa → `400 Bad Request`

---

### UC15 — Consulta da Turma por ID
**Escopo:** Classroom
**Ator Primário:** Diretor / Administrador
**Pré-condição:** Turma cadastrada no sistema

**Cenário principal de sucesso:**
1. O sistema busca `Classroom` por ID
2. O sistema valida que a turma existe
3. O sistema retorna `ClassroomOut`

**Garantia de sucesso:** Turma localizada para visualização ou edição

**Extensões:**
- `1a` — Turma não encontrada → `404 Not Found`

---

### UC16 — Listagem de Turmas por Escola
**Escopo:** Classroom
**Ator Primário:** Diretor / Administrador
**Pré-condição:** Identificador da escola informado

**Cenário principal de sucesso:**
1. O sistema lista turmas associadas à escola
2. O sistema retorna a coleção de `ClassroomOut`

**Garantia de sucesso:** Lista de turmas por escola disponível

**Extensões:**
- `1a` — Nenhuma turma encontrada → lista vazia retornada

---

### UC17 — Atualização da Turma
**Escopo:** Classroom
**Ator Primário:** Diretor / Administrador
**Pré-condição:** Turma existente no sistema

**Cenário principal de sucesso:**
1. O sistema busca `Classroom` por ID
2. O sistema aplica alterações válidas no curso
3. O sistema salva a turma e retorna `ClassroomOut`

**Garantia de sucesso:** Turma atualizada e persistida

**Extensões:**
- `1a` — Turma não encontrada → `404 Not Found`

---

### UC18 — Desativação da Turma
**Escopo:** Classroom
**Ator Primário:** Diretor / Administrador
**Pré-condição:** Turma existente no sistema

**Cenário principal de sucesso:**
1. O sistema busca `Classroom` por ID
2. O sistema marca a turma como inativa
3. O sistema salva a alteração e retorna `ClassroomOut`

**Garantia de sucesso:** Turma desativada e não participa de novos cadastros

**Extensões:**
- `1a` — Turma não encontrada → `404 Not Found`

---

### UC19 — Consulta do Estudante por ID
**Escopo:** Users.Student
**Ator Primário:** Coordenador / Diretor
**Pré-condição:** Estudante cadastrado no sistema

**Cenário principal de sucesso:**
1. O sistema busca o estudante por ID
2. O sistema valida que o estudante existe
3. O sistema retorna os dados do estudante com conta associada

**Garantia de sucesso:** Estudante localizado e exibido com informações completas

**Extensões:**
- `1a` — Estudante não encontrado → `404 Not Found`

---

### UC20 — Atualização do Estudante
**Escopo:** Users.Student
**Ator Primário:** Coordenador / Diretor
**Pré-condição:** Estudante existente no sistema

**Cenário principal de sucesso:**
1. O sistema busca o estudante por ID
2. O sistema aplica alterações válidas na turma ou data de nascimento
3. O sistema salva o estudante e retorna os dados atualizados

**Garantia de sucesso:** Dados do estudante atualizados e persistidos

**Extensões:**
- `1a` — Estudante não encontrado → `404 Not Found`

---

### UC21 — Desativação do Estudante
**Escopo:** Users.Student
**Ator Primário:** Coordenador / Diretor
**Pré-condição:** Estudante existente com conta vinculada

**Cenário principal de sucesso:**
1. O sistema busca o estudante por ID
2. O sistema desativa a conta associada
3. O sistema salva as alterações e retorna o estudante inativo

**Garantia de sucesso:** Estudante desativado e bloqueado para acesso

**Extensões:**
- `1a` — Estudante não encontrado → `404 Not Found`

---

### UC22 — Cadastro do Coordenador
**Escopo:** Users.Coordinator
**Ator Primário:** Diretor
**Pré-condição:** E-mail não pode estar cadastrado e escola deve existir

**Cenário principal de sucesso:**
1. O sistema valida o e-mail e a escola vinculada
2. O sistema cria a conta de usuário com perfil de coordenador
3. O sistema persiste o coordenador e retorna o registro completo

**Garantia de sucesso:** Coordenador cadastrado e vinculado à escola

**Extensões:**
- `1a` — E-mail já cadastrado → `409 Conflict`
- `1b` — Escola não encontrada ou inativa → `400 Bad Request`

---

### UC23 — Consulta do Coordenador por ID
**Escopo:** Users.Coordinator
**Ator Primário:** Diretor / Administrador
**Pré-condição:** Coordenador cadastrado no sistema

**Cenário principal de sucesso:**
1. O sistema busca o coordenador por ID
2. O sistema valida que o coordenador existe
3. O sistema retorna os dados do coordenador

**Garantia de sucesso:** Coordenador localizado corretamente

**Extensões:**
- `1a` — Coordenador não encontrado → `404 Not Found`

---

### UC24 — Desativação do Coordenador
**Escopo:** Users.Coordinator
**Ator Primário:** Diretor / Administrador
**Pré-condição:** Coordenador existente com conta de usuário vinculada

**Cenário principal de sucesso:**
1. O sistema busca o coordenador por ID
2. O sistema desativa a conta de usuário associada
3. O sistema salva as alterações e retorna o coordenador inativo

**Garantia de sucesso:** Coordenador desativado e sem acesso ao sistema

**Extensões:**
- `1a` — Coordenador não encontrado → `404 Not Found`

---

### UC25 — Cadastro do Diretor
**Escopo:** Users.Director
**Ator Primário:** Administrador
**Pré-condição:** E-mail não pode estar cadastrado e escola deve existir

**Cenário principal de sucesso:**
1. O sistema valida o e-mail e a escola vinculada
2. O sistema cria a conta de usuário com perfil de diretor
3. O sistema persiste o diretor e retorna o registro completo

**Garantia de sucesso:** Diretor cadastrado e vinculado à escola

**Extensões:**
- `1a` — E-mail já cadastrado → `409 Conflict`
- `1b` — Escola não encontrada ou inativa → `400 Bad Request`

---

### UC26 — Consulta do Diretor por ID
**Escopo:** Users.Director
**Ator Primário:** Administrador
**Pré-condição:** Diretor cadastrado no sistema

**Cenário principal de sucesso:**
1. O sistema busca o diretor por ID
2. O sistema valida que o diretor existe
3. O sistema retorna os dados do diretor

**Garantia de sucesso:** Diretor localizado corretamente

**Extensões:**
- `1a` — Diretor não encontrado → `404 Not Found`

---

### UC27 — Desativação do Diretor
**Escopo:** Users.Director
**Ator Primário:** Administrador
**Pré-condição:** Diretor existente com conta de usuário vinculada

**Cenário principal de sucesso:**
1. O sistema busca o diretor por ID
2. O sistema desativa a conta de usuário associada
3. O sistema salva as alterações e retorna o diretor inativo

**Garantia de sucesso:** Diretor desativado e sem acesso ao sistema

**Extensões:**
- `1a` — Diretor não encontrado → `404 Not Found`

---

## ✨ Funcionalidades Principais

- **Cadastro de turmas e alunos** com vinculação ao reconhecimento facial
- **Monitoramento contínuo** via câmeras de segurança já instaladas
- **Painel web** com alertas ativos e histórico emocional individual de cada aluno
- **Relatórios** organizados por aluno, turma e turno
- **Notificações duplas** — painel web + mensagem automática via WhatsApp
- **Sem armazenamento de imagens** — apenas dados analíticos são persistidos

---

## 🚀 Instalação do Backend

### Requisitos
- Python 3.12+
- [uv](https://docs.astral.sh/uv/) instalado globalmente
- Docker (opcional, recomendado para ambiente consistente)
- `docker compose` disponível se optar pelo container

### Instalação do `uv` (caso ainda não tenha)

**Linux / macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

> O `uv` deve ser instalado **globalmente**, fora de qualquer ambiente virtual. Ele é a ferramenta responsável por criar e gerenciar o `.venv` do projeto.

---

### Instalação local

1. Entre na pasta do backend:
   ```bash
   cd backend
   ```
2. Crie e ative o ambiente virtual:
   ```bash
   uv venv .venv
   source .venv/bin/activate  # Linux/macOS
   # ou
   .venv\Scripts\activate     # Windows
   ```
3. Instale as dependências usando o lockfile existente:
   ```bash
   uv sync --frozen --no-dev --no-install-project --no-cache
   ```
4. Execute as migrações do Django:
   ```bash
   python manage.py migrate
   ```
5. Inicie o servidor local:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

---

### Instalação com Docker Compose

1. Na raiz do projeto, rode:
   ```bash
   docker compose up --build backend
   ```
2. Acesse o backend em:
   ```
   http://localhost:8000
   ```

---

### Variáveis de ambiente

O backend carrega variáveis de ambiente via `python-dotenv`. Os valores padrão estão definidos em `backend/config/settings.py`, mas você pode criar um arquivo `.env` na raiz do `backend` com as seguintes chaves:

| Variável | Descrição |
|---|---|
| `SECRET_KEY` | Chave secreta do Django |
| `ALGORITHM` | Algoritmo de assinatura JWT (ex: `HS256`) |
| `JWT_EXP_MINUTES` | Tempo de expiração do token de acesso (em minutos) |
| `JWT_EXP_DAYS` | Tempo de expiração do refresh token (em dias) |
| `DEBUG` | Modo de depuração (`True` em dev, `False` em produção) |

---

## 🗺️ Roadmap

### ✅ MVP — em desenvolvimento
- Cadastro de turmas e alunos
- Reconhecimento facial com InsightFace
- Detecção e rastreamento com YOLO + DBSCAN
- Painel web inicial em Django
- Notificações via WhatsApp (WAHA)

### 🔜 V2
- App mobile para gestores
- Módulo de autorrelato para estudantes
- Testes em ambiente escolar real com escolas parceiras

### 🔮 V3
- Módulo de gestão centralizada para secretarias de educação
- Expansão para ensino superior e centros socioeducativos

---

## Como Acessar os Endpoints

Os endpoints ficam disponíveis nos prefixos:

| Prefixo | App |
|---|---|
| `/api/accounts` | Accounts |
| `/api/schools` | Schools |
| `/api/school` | Schools |
| `/api/student` | Users |
| `/api/coordinator` | Users |
| `/api/director` | Users |

> A documentação interativa automática do Django Ninja estará disponível em `/api/docs`.

---

## 🔒 Ética e Privacidade

- **Nenhuma imagem é armazenada** — o sistema acessa o feed ao vivo do DVR e processa em tempo real
- Apenas informações analíticas e alertas são persistidos no banco
- Os dados são utilizados **exclusivamente pelos gestores escolares**
- A adoção prevê reuniões com pais e responsáveis para apresentação transparente do sistema
- A escola já monitora os alunos com câmeras de segurança; o empatIA adiciona uma finalidade de **bem-estar emocional** a essa infraestrutura existente

---

## 💰 Modelo de Negócio

**Licença anual por escola** — inclui acesso à plataforma, atualizações e suporte técnico.

| Métrica | Valor |
|---|---|
| Preço por aluno | R$ 2,00 / mês |
| Escola com 500 alunos | R$ 12.000 / ano |
| Custo operacional estimado | ~R$ 500 / escola / ano |
| 50 escolas atendidas | R$ 600.000 / ano (receita bruta) |

Para governos estaduais e municipais: negociação por rede de ensino com base no total de alunos matriculados.

**Mercado potencial no Piauí:**

| Segmento | Descrição |
|---|---|
| **TAM** | ~3.800 escolas públicas |
| **SAM** | Escolas estaduais de ensino médio |
| **Beachhead** | CETI Liceu Parnaibano |

---

## 🏫 Contexto Institucional

Desenvolvido na **1ª Gerência Regional de Educação (Parnaíba — PI)**, pelo CETI Liceu Parnaibano.

| Nome | Papel |
|---|---|
| Antonio Carlos dos Santos da Silva | Desenvolvedor IA |
| Arthur França Silva | Desenvolvedor Back + IA |
| João Miguel Barros da Silva | Desenvolvedor Front |
| Pablo de Jesus dos Santos Dionisio de Oliveira | Desenvolvedor Front |
| Rian da Silva Sousa | Desenvolvedor Front |
| Marcos José Souza do Nascimento | Orientador |

---

## 📚 Referências

- IBGE. *Pesquisa Nacional de Saúde do Escolar (PeNSe) 2024*. Rio de Janeiro: IBGE, 2026.
- TODOS PELA EDUCAÇÃO. *Anuário Brasileiro da Educação Básica 2024*. São Paulo: Editora Moderna, 2024.
- PRADO, E. A. M; FELIPPE, J. M. S. *Sofrimento psíquico, educação escolar e juventude*. Revista Tempos e Espaços em Educação, v. 16, n. 35, 2023.
- MENDONÇA, Leone da Silva et al. *O ambiente escolar como fator determinante no desenvolvimento socioemocional de crianças*. REMI, v. 2, n. 05, 2026.
- PEDROSA, Valéria da Silva Ferreira et al. *Educação e saúde mental na escola*. REVISTA DELOS, v. 19, n. 76, 2026.

---

> *"O empatIA não pretende substituir o olhar humano — pretende potencializá-lo."*