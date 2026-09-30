# Relatório final — abnt-skill v1.0

## 1. Estrutura final

Repositório = a skill (a pasta `abnt-skill` É instalável em
`~/.claude/skills/` ou `.claude/skills/`):

```text
abnt-skill/
├── SKILL.md                  # roteador /abnt (frontmatter name: abnt)
├── README.md / INSTALL.md / LICENSE
├── standards/abnt/           # normas.md, formatacao.md, citacoes.md,
│                             # referencias.md, numeracao-sumario-resumo.md,
│                             # artigos-projetos.md (+README com fontes)
├── standards/school/         # documents/ + presentations/ (regra 10-20-30…)
├── applications/             # word/ powerpoint/ excel/ outlook/ onenote/
│                             # access/ + office-oficial.md
├── design/                   # documents/ presentations/ spreadsheets/
├── formats/                  # pdf/ docx/ xlsx/ pptx/ rtf/ csv/ txt/
├── workflows/                # 6 fluxos prontos de ponta a ponta
├── assets/checklists/        # entrega.md (QA obrigatório)
├── scripts/validate.py       # validação estática (exit 0 = OK)
├── tests/TESTES.md           # protocolo + casos de teste
└── docs/                     # INTEGRACAO-OFFICE.md, RELATORIO-FINAL.md
```

## 2. Mecanismo real do `/abnt`

- **Comando:** campo oficial `name: abnt` no frontmatter do `SKILL.md`
  ("name sets the command"); pasta instalada `abnt-skill` — o nome do diretório
  também invoca, logo `/abnt-skill` é alias automático. Nenhum sistema próprio.
- **Fallback automático:** `description` + `when_to_use` (padrões de invocação
  mantidos: `user-invocable` e auto-invocação ativos) carregam a skill quando o
  contexto indica ABNT, trabalho acadêmico, TCC, seminário, slides, formatação
  ou conversão de material — mesmo sem digitar `/abnt`.

## 3. Dependência da Office Skill oficial

Não existe dependência declarativa skill→skill na especificação (ver
[INTEGRACAO-OFFICE.md](INTEGRACAO-OFFICE.md)). Implementado o mecanismo oficial
possível: documentação dos nomes/capacidades reais (`docx`, `pdf`, `pptx`,
`xlsx`), delegação operacional em runtime, verificação de disponibilidade e
modo orientado como fallback. Zero duplicação (validado por script).

## 4. Subskills/módulos

Módulos internos em Markdown carregados sob demanda (não são skills invocáveis
separadas — identidade única `/abnt`): 6 de ABNT, 2 da escola, 6 aplicativos +
integração Office, 3 de design, 7 de formatos, 6 fluxos, 1 checklist de entrega.

## 5. Regras ABNT implementadas

NBR 14724 (estrutura, A4, margens 3/2/3/2, fonte 12, 1,5, paginação, filete
5 cm, ilustrações), 10520 (autor-data/numérico, diretas/indiretas/apud),
6023 (ordem alfabética, espaçamento; edição 2018×2025 marcada p/ confirmar),
6024 (numeração sem sinal), 6027 (sumário), 6028 (resumo 150–500, 3–5
palavras-chave), 6022 (artigos), 15287 (projetos). Todas com fontes citadas;
convenções de manuais (tipo de fonte, recuo) marcadas como convenções.

## 6. Regras escolares implementadas

10-20-30 flexível (≈10 slides, ≈20 min, máx. 30 pt); texto 20–25 pt; nunca
reduzir letra para caber excesso; composição centralizada tradicional; paleta
de 3 cores; proibição de elementos inventados; prioridade a
infográfico/diagramas/gráficos/imagens reais; `Fonte:` obrigatória para todo
material externo.

## 7. Regras de design

Hierarquia + respiro + consistência de estilos (documentos); grade
título→conteúdo→fonte, escala 20–25/30, contraste de projeção, antipadrões
(apresentações); tabela-fato limpa, condicional com propósito, gráficos honestos
(planilhas).

## 8. Testes executados

- `scripts/validate.py`: frontmatter, limites da spec, <500 linhas, links
  internos, identidade única, NBRs restritas, anti-duplicação Office, módulos
  presentes → **OK** (ver [tests/TESTES.md](../tests/TESTES.md)).
- Protocolo comportamental dos 6 casos `/abnt` documentado para execução no
  Claude Code com critérios de aceite (a sandbox de build não executa o
  Claude Code; resultados devem ser registrados ao rodar).

## 9. Limitações

Outlook/OneNote/Access e RTF/CSV/TXT sem skill oficial (modo orientado); textos
integrais das NBRs não incluídos (direitos autorais — resumos com fontes);
edição vigente da NBR 6023 a confirmar (fontes divergem 2018×2025); upload para
claude.ai/API exige pasta `abnt` + frontmatter só com campos da spec (ver
INSTALL.md); estética de slides não é regida por NBR (camadas escola+design).

## 10. Exemplos reais de invocação

```text
/abnt Crie um documento baseado neste PDF.
/abnt Faça um PowerPoint baseado neste PDF.
/abnt Transforme este documento em uma apresentação.
/abnt Organize estes dados em uma planilha.
/abnt Faça um trabalho acadêmico seguindo ABNT.
/abnt Faça uma apresentação seguindo as orientações da escola.
```
