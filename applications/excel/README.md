# Excel — planilhas (via skill oficial `xlsx`)

**Quando usar:** dados, tabelas, cálculos, gráficos, análise, planilhas.

## O que a abnt-skill decide (antes de delegar)

1. Modelo: uma tabela-fato limpa por aba (cabeçalho único, sem células
   mescladas no dado), abas separadas para parâmetros, cálculos e apresentação.
2. Organização: normalizar CSV/dados soltos (tipos, datas, textos), remover
   sujeira, validar totais; documentar a origem dos dados.
3. Formatação: cabeçalho legível, números com formato adequado, formatação
   condicional com moderação, impressão configurada quando o destino for papel.
4. Gráficos/tabelas **quando necessários**: um gráfico por mensagem, eixos
   rotulados, sem 3D/distorsão; cada visual com fonte dos dados.
5. Design: [design/spreadsheets/](../../design/spreadsheets/README.md).

## O que delegar à skill oficial `xlsx`

Criação/edição do `.xlsx`: estrutura de abas, fórmulas (sem erro), validação,
gráficos, formatação condicional, tabelas dinâmicas, limpeza de dados brutos.

## Checklist específico

- [ ] Fórmulas recalculam sem erro; totais conferem com a fonte
- [ ] Cabeçalhos claros; nenhuma informação crítica só por cor
- [ ] Fonte dos dados registrada (aba "Sobre"/"Fontes" + `Fonte:` nos impressos)
- [ ] Checklist geral: [assets/checklists/entrega.md](../../assets/checklists/entrega.md)
