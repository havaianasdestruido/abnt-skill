# Integração com as skills oficiais de Office — descoberta e decisão

## O que foi descoberto (verificado em fontes oficiais)

1. **Não existe "uma Office Skill" única.** Existem **4 skills oficiais da
   Anthropic**: `docx`, `pdf`, `pptx`, `xlsx`, publicadas para referência em
   `github.com/anthropics/skills` e **pré-incluídas no Claude** (o README do
   repositório e a documentação afirmam que versões dessas skills acompanham o
   produto; no Claude Code elas aparecem no menu `/skills`, podendo vir
   sincronizadas da conta, incluindo built-ins como `pdf` e `xlsx`).
2. **Licença:** *source-available* (referência), diferente das demais skills do
   repositório (Apache-2.0).
3. **Capacidades** (resumo; detalhe em
   [applications/office-oficial.md](../applications/office-oficial.md)):
   `docx` cria/edita Word; `pptx` cria/edita PowerPoint; `xlsx` cria/analisa
   Excel; `pdf` extrai/manipula/gera PDFs.
4. **Na API do Claude**, usam-se IDs curtos (`docx`, `pdf`, `pptx`, `xlsx`,
   tipo `anthropic`, versão `latest`) no parâmetro `container.skills` com a
   ferramenta de execução de código; arquivos saem pela Files API.
5. **Limites:** não cobrem Outlook, OneNote, Access, RTF, CSV ou TXT.

## Por que não há `depends_on` / declaração formal

- A especificação Agent Skills (`SKILL.md`) não define campo de dependência
  skill→skill. Campos portáteis: `name, description, license, compatibility,
  metadata, allowed-tools`.
- O campo `dependencies` existe apenas no manifesto de plugin
  (`.claude-plugin/plugin.json`) e resolve **plugin→plugin dentro de um
  marketplace**. As skills oficiais de documentos não são um plugin de
  marketplace instalável por esse mecanismo.
- Qualquer `depends_on: office-skill` seria um mecanismo inventado — proibido
  pelos requisitos do projeto. A integração oficial possível é:
  **documentar (esta página + `applications/office-oficial.md`) → delegar em
  runtime → verificar disponibilidade → fallback orientado.**

## Por que não distribuir como plugin

Skills de plugin são namespaced (`/plugin:skill`); distribuir como plugin
impediria o comando simples `/abnt`. Por isso a distribuição é como skill
pessoal/projeto: pasta `abnt-skill` + `name: abnt` (ver [INSTALL.md](../INSTALL.md)).

## Separação garantida (anti-duplicação)

- A `abnt-skill` **não contém** código de manipulação de DOCX/XLSX/PPTX/PDF
  (o validador `scripts/validate.py` falha se qualquer script local importar
  `zipfile`, `python-docx`, `openpyxl`, `pptx`, `pypdf` etc.).
- Toda criação/leitura/edição de arquivos Office é delegada às skills oficiais
  em runtime, com as especificações (ABNT + escola + design) decididas aqui.
