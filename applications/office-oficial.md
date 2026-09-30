# Integração com as skills oficiais de Office

## Descoberta (verificada, nada inventado)

Não existe "uma Office Skill" única. O que existe são **4 skills oficiais da
Anthropic**, mantidas no repositório público `github.com/anthropics/skills`
(pastas `skills/docx`, `skills/pdf`, `skills/pptx`, `skills/xlsx`), que
**acompanham o Claude** (documentação e README do repositório confirmam que
versões dessas skills vêm pré-incluídas). Licença: *source-available* (código
visível para referência, não open-source como as demais do repositório).

| Skill oficial | ID | Capacidades |
|---|---|---|
| `docx` | `docx` | criar, ler, editar Word (.docx/.dotx): estilos, sumário, cabeçalhos/rodapés, numeração de páginas, tabelas, imagens, controle de alterações |
| `pptx` | `pptx` | criar/editar apresentações (.pptx/.potx): layouts mestres, gráficos, notas do orador; extração de texto |
| `xlsx` | `xlsx` | criar/analisar planilhas: fórmulas sem erro, gráficos, formatação condicional, tabelas dinâmicas; limpeza de dados tabulares |
| `pdf` | `pdf` | extração de texto/tabelas, mesclar/dividir, formulários, OCR de digitalizados; geração de PDFs formatados |

Na API do Claude, os IDs curtos (`docx`, `pdf`, `pptx`, `xlsx`, tipo
`anthropic`, versão `latest`) são passados no parâmetro `container.skills`
junto à ferramenta de execução de código, e os arquivos gerados são baixados
pela Files API. No Claude Code, elas aparecem no menu `/skills` (podem vir
sincronizadas da conta claude.ai, incluindo built-ins como `pdf` e `xlsx`).

## Por que não há declaração formal de dependência

A especificação Agent Skills (`SKILL.md`) **não define nenhum campo de
dependência skill→skill** — os únicos campos portáteis são `name, description,
license, compatibility, metadata, allowed-tools`. O campo `dependencies` só
existe no manifesto de **plugin** (`.claude-plugin/plugin.json`) e resolve
plugin→plugin dentro de um marketplace; as skills oficiais de documentos não
são um plugin de marketplace instalável por esse mecanismo. Declarar algo como
`depends_on: office-skill` seria **inventar um mecanismo** — por isso a
`abnt-skill` não o faz. A integração correta e oficial é:

1. **Documentação** desta página (nomes reais, capacidades, limites);
2. **Delegação em runtime**: a `abnt-skill` decide o *quê/como* e invoca as
   skills oficiais para o *operacional* (Claude Code carrega múltiplas skills
   na mesma sessão conforme a descrição de cada uma);
3. **Verificação + fallback** (abaixo) quando alguma skill oficial ausente.

## Separação de responsabilidades (obrigatória)

- **Skills oficiais** → criar, ler, editar e manipular arquivos (OOXML,
  fórmulas, extração de PDF, recálculo). A `abnt-skill` **não** contém scripts
  de manipulação de DOCX/XLSX/PPTX/PDF — nenhuma duplicação.
- **abnt-skill** → roteamento (`/abnt`), estrutura acadêmica, regras ABNT,
  orientações da escola, design, atribuição de fontes e checklist de entrega.

## Verificação de disponibilidade (runtime)

1. Liste as skills ativas (`/skills`) e confirme `docx`, `pdf`, `pptx`, `xlsx`.
2. Ausente? Oriente o usuário a ativá-la nas Skills da conta (claude.ai) e
   prossiga em **modo orientado**: entregue o conteúdo pronto (Markdown) +
   roteiro passo a passo de montagem no aplicativo, deixando claro o que não
   foi manipulado diretamente.
3. Nunca alegue ter criado/editado um arquivo que só foi descrito em texto.

## O que as skills oficiais NÃO cobrem

Outlook, OneNote e Access não possuem skill oficial: os módulos
[outlook/](outlook/README.md), [onenote/](onenote/README.md) e
[access/](access/README.md) operam sempre em modo orientado. RTF/CSV/TXT são
formatos genéricos sem skill dedicada (ver [formats/](../formats/README.md)).
