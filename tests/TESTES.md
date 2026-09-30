# Testes da abnt-skill

## A. Validação estática (automatizada — executar na sandbox)

```bash
python3 scripts/validate.py
python3 tests/test_frontmatter.py
```

Checagens (`validate.py`): frontmatter parseável, tipos decodificados válidos e
dentro dos limites da spec (`name` kebab-case `abnt`, `description` ≤1024,
`compatibility` ≤500, sem campos desconhecidos); `SKILL.md` <500 linhas;
`$ARGUMENTS` presente; links internos resolvendo; identidade única (sem
`office-skills`, `abnt-office`, `school-office`, `academic-office`); NBRs
restritas à lista pesquisada; scripts sem manipulação Office; módulos
obrigatórios presentes.

Regressão (`test_frontmatter.py`): valores com aspas simples/duplas, mapa
`metadata`, colchetes balanceados; rejeição de YAML malformado (sem fechamento,
linha sem dois-pontos, sequência/mapa não fechados, bloco multilinha,
indentação fora de `metadata`) e de tipos decodificados inválidos.

**Resultado registrado:** `RESULTADO: OK -- todas as checagens passaram.` em
ambos os scripts (exit 0; ver log de execução no commit; reexecutar após
qualquer alteração).

## B. Protocolo comportamental (executar no Claude Code)

Pré-requisito: skill instalada (ver [INSTALL.md](../INSTALL.md)) e Claude Code
reiniciado. Para cada caso, verificar os critérios de aceite:

| # | Caso | Critérios de aceite |
|---|---|---|
| 1 | `/abnt Crie um documento baseado neste PDF.` (+ PDF anexado) | aciona `/abnt`; lê PDF via skill `pdf`; gera DOCX via `docx`; estrutura ABNT; citações/referências consistentes; fontes registradas |
| 2 | `/abnt Faça um PowerPoint baseado neste PDF.` (+ PDF) | aciona; interpreta e seleciona conteúdo (≈10 slides); PPTX via `pptx`; texto 20–25 pt, nada >30 pt; centralizado; ≤3 cores; sem enchimento; `Fonte:` em imagens/dados; fala nas notas |
| 3 | `/abnt Transforme este documento em uma apresentação.` (+ DOCX) | aciona; comprime (não cola texto); tabelas densas viram gráfico/resumo; mesmas regras visuais do caso 2 |
| 4 | `/abnt Organize estes dados em uma planilha.` (+ CSV/XLSX) | aciona; normaliza (cabeçalho, tipos, sujeira); XLSX via `xlsx`; fórmulas sem erro; gráficos só se necessários, honestos; aba Sobre/Fontes |
| 5 | `/abnt Faça um trabalho acadêmico seguindo ABNT.` | aciona; aplica NBR 14724 (margens, 12 pt, 1,5, paginação), 10520, 6023, 6024, 6027, 6028; sem NBR/regra inventada; dúvidas de edição comunicadas |
| 6 | `/abnt Faça uma apresentação seguindo as orientações da escola.` | aciona; 10-20-30 flexível; 20–25 pt; centralizada; ≤3 cores; visuais funcionais reais; fontes atribuídas; sem elementos inventados |
| 7 | Pedido sem comando: `preciso formatar meu TCC na ABNT` | skill carregada automaticamente (fallback); mesmo comportamento do caso 5 |
| 8 | `/abnt-skill ...` (alias) | funciona igual ao `/abnt` |
| 9 | Pedido Outlook/OneNote/Access | modo orientado declarado; conteúdo pronto + passos manuais; nenhuma afirmação falsa de manipulação |
| 10 | Skill oficial ausente (desativar `pptx` p/ teste) | fallback orientado declarado (Markdown + roteiro); sem simular o PPTX |

Registro de execução: data, versão do Claude Code, PASS/FAIL por caso e
observações — anexar ao commit/PR que liberar a versão.
