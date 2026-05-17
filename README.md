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
| `password` | string | hash |
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
| `user` | FK → User | — |
| `expire_at` | datetime | — |
| `created_at` | datetime | — |
| `revoked` | bool | — |

### `Schools.School`

| Campo | Tipo | Observação |
|---|---|---|
| `id` | UUID | PK |
| `name` | string | — |
| `cnpj` | string | validado via value object |
| `logo` | file | upload |
| `gre` | string | Gerência Regional de Educação |
| `created_at` | datetime | — |
| `deleted_at` | datetime | soft delete |

### `Schools.NucleosGroup`

| Campo | Tipo | Observação |
|---|---|---|
| `id` | UUID | PK |
| `name` | string | — |
| `school` | FK → School | — |
| `created_at` | datetime | — |
| `deleted_at` | datetime | soft delete |

### `Users.Student`

| Campo | Tipo | Observação |
|---|---|---|
| `id` | UUID | PK |
| `user` | OneToOne → Accounts.User | — |
| `classroom` | FK → Classroom | — |
| `date_birth` | date | — |
| `photo` | file | — |
| `vector_facial` | JSON | embeddings gerados pelo InsightFace |

### `Users.Coordinator`

| Campo | Tipo | Observação |
|---|---|---|
| `id` | UUID | PK |
| `user` | OneToOne → Accounts.User | — |
| `nucleos_group` | FK → NucleosGroup | — |

### `Users.Director`

| Campo | Tipo | Observação |
|---|---|---|
| `id` | UUID | PK |
| `user` | OneToOne → Accounts.User | — |
| `school` | OneToOne → Schools.School | — |

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

**Garantia de sucesso:** Escola cadastrada e disponível para associar núcleos e diretores

**Extensões:**
- `2a` — CNPJ inválido → `400 Bad Request`
- `2b` — Escola já cadastrada → `409 Conflict`

---

### UC05 — Cadastro do Núcleo Gestor
**Escopo:** Schools.NucleosGroup  
**Ator Primário:** Diretor  
**Pré-condição:** Escola existente no sistema

**Cenário principal de sucesso:**
1. O sistema recebe nome do núcleo e ID da escola
2. O sistema valida a existência da escola
3. O sistema persiste `Schools.NucleosGroup` e retorna `201`

**Garantia de sucesso:** Núcleo gestor criado e vinculado à escola

**Extensões:**
- `2a` — Escola não encontrada → `404 Not Found`

---

## ✨ Funcionalidades Principais

- **Cadastro de turmas e alunos** com vinculação ao reconhecimento facial
- **Monitoramento contínuo** via câmeras de segurança já instaladas
- **Painel web** com alertas ativos e histórico emocional individual de cada aluno
- **Relatórios** organizados por aluno, turma e turno
- **Notificações duplas** — painel web + mensagem automática via WhatsApp
- **Sem armazenamento de imagens** — apenas dados analíticos são persistidos

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
| `/api/nucleos_group` | Schools |
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
| Antonio Carlos dos Santos da Silva | Desenvolvedor |
| Arthur França Silva | Desenvolvedor |
| João Miguel Barros da Silva | Desenvolvedor |
| Pablo de Jesus dos Santos Dionisio de Oliveira | Desenvolvedor |
| Rian da Silva Sousa | Desenvolvedor |
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