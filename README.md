# abnt-skill

Uma skill única para produção acadêmica e profissional com normas ABNT,
orientações da escola e design de documentos — sobre as skills oficiais de
Office do Claude.

- **Identidade única:** `abnt-skill` (sempre com hífen; sem nomes alternativos).
- **Comando:** `/abnt` — roteamento automático, o usuário nunca escolhe módulo interno.
- **Camada inteligente:** esta skill decide estrutura, formatação, normas e design.
- **Camada operacional:** as skills oficiais da Anthropic (`docx`, `pdf`, `pptx`,
  `xlsx`) criam, leem e editam os arquivos.

```text
                     /abnt
                       │
                       ▼
                 ┌───────────┐
                 │ abnt-skill│  ← inteligência: ABNT + escola + design
                 └─────┬─────┘
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
        Word      PowerPoint       Excel   (+ Outlook/OneNote/Access orientados)
         │             │             │
         └─────────────┼─────────────┘
                       ▼
        Skills oficiais (docx/pdf/pptx/xlsx)  ← operação: arquivos
```

## Uso

```text
/abnt Crie um documento baseado neste PDF.
/abnt Faça um PowerPoint baseado neste PDF.
/abnt Transforme este documento em uma apresentação.
/abnt Organize estes dados em uma planilha.
/abnt Faça um trabalho acadêmico seguindo ABNT.
/abnt Faça uma apresentação seguindo as orientações da escola.
```

Sem o comando, a skill também é carregada automaticamente quando o pedido
menciona ABNT, trabalho acadêmico, TCC, seminário, slides, formatação de
documento ou conversão de material em trabalho/apresentação/planilha.

## Instalação

Guia completo em [INSTALL.md](INSTALL.md). Resumo:

```bash
# Pessoal (vale para todos os seus projetos):
mkdir -p ~/.claude/skills
cp -r /caminho/para/abnt-skill ~/.claude/skills/abnt-skill

# Ou por projeto (dentro do repositório, versionado em git):
mkdir -p .claude/skills
cp -r /caminho/para/abnt-skill .claude/skills/abnt-skill
```

Reinicie o Claude Code e digite `/abnt`. O comando `/abnt-skill` funciona como
alias (nome do diretório). As skills oficiais `docx`/`pdf`/`pptx`/`xlsx` já
acompanham o Claude — confira no menu `/skills`.

## Estrutura

```text
abnt-skill/              ← este repositório (a pasta É a skill)
├── SKILL.md             ← roteador: comando /abnt + decisão automática
├── standards/
│   ├── abnt/            ← NBRs pesquisadas (com fontes, sem invenção)
│   └── school/
│       ├── documents/   ← orientações da escola: documentos
│       └── presentations/ ← orientações da escola: apresentações
├── applications/
│   ├── word/ powerpoint/ excel/ outlook/ onenote/ access/
│   └── office-oficial.md ← integração com as skills oficiais
├── design/
│   ├── documents/ presentations/ spreadsheets/
├── formats/
│   ├── pdf/ docx/ xlsx/ pptx/ rtf/ csv/ txt/
├── workflows/           ← fluxos prontos (PDF→DOCX, PDF→PPTX, DOC→PPTX…)
├── assets/checklists/   ← checklist final de entrega
├── scripts/             ← validação estática (não manipula Office)
├── tests/               ← protocolo de testes + casos
└── docs/                ← integração Office, relatório final, testes
```

Mecanismos reais utilizados (nada inventado): skill `SKILL.md` + `name: abnt`
para o comando `/abnt`; `description`/`when_to_use` para carregamento
automático; delegação operacional às skills oficiais. Detalhes em
[docs/INTEGRACAO-OFFICE.md](docs/INTEGRACAO-OFFICE.md) e
[docs/RELATORIO-FINAL.md](docs/RELATORIO-FINAL.md).

## Licença

Apache-2.0 — ver [LICENSE](LICENSE). Os textos integrais das normas ABNT/NBR
são protegidos por direitos autorais e **não** estão incluídos aqui; os módulos
em `standards/abnt/` resumem regras a partir de guias públicos, sempre citados.
