---
name: abnt
description: Produz e formata trabalhos acadêmicos ABNT, apresentações escolares e planilhas (Word, PowerPoint, Excel). Use quando o usuário pedir ABNT, NBR, trabalho acadêmico, TCC, monografia, artigo, formatação acadêmica, apresentação escolar, seminário, aula, slides, documento Word, planilha, relatório, ou conversão de PDF/documento/dados em trabalho, apresentação ou planilha.
when_to_use: O usuário invocou /abnt, ou a tarefa menciona ABNT, NBR, TCC, trabalho acadêmico, seminário, slides escolares, formatação de documento, organização de planilha para trabalho, transformar PDF em documento/apresentação, transformar documento em apresentação.
argument-hint: [tarefa: documento | apresentação | planilha | conversão]
license: Apache-2.0
compatibility: Claude Code com as skills oficiais de documentos (docx, pptx, xlsx, pdf). Scripts de validação opcionais exigem Python 3.
metadata:
  identidade: abnt-skill
  versao: "1.0"
  idioma: pt-BR
---

# abnt-skill

Skill única de produção acadêmica e profissional. O usuário interage **somente**
com a `abnt-skill` (comando `/abnt`); os módulos internos abaixo trabalham
silenciosamente. Nunca peça ao usuário para escolher um módulo interno.

> Tarefa recebida: **$ARGUMENTS**
>
> Se a tarefa estiver vazia, peça em uma frase o que deve ser produzido
> (documento, apresentação ou planilha) e a partir de qual material.

## 1. Roteamento automático

Para toda tarefa, identifique nesta ordem, sem perguntar o óbvio:

1. **Objetivo** — documento, apresentação, planilha, e-mail/nota/banco de dados
   ou conversão entre formatos.
2. **Formato de entrada** — PDF, DOCX, XLSX, PPTX, RTF, CSV, TXT ou dados soltos.
   Regras por formato em [formats/](formats/README.md).
3. **Formato desejado** — inferido do pedido ("trabalho" → DOCX, "slides" →
   PPTX, "organize os dados" → XLSX). Na dúvida, pergunte em uma frase.
4. **Aplicativo** — pela tabela abaixo (detalhes em [applications/](applications/README.md)):

   | Pedido | Aplicativo |
   |---|---|
   | trabalho, relatório, artigo, texto acadêmico, documento formatado | Word (DOCX) |
   | apresentação, seminário, aula, slides | PowerPoint (PPTX) |
   | dados, tabelas, cálculos, gráficos, análise | Excel (XLSX) |
   | e-mail, calendário, reunião | Outlook (orientação — ver limites) |
   | notas, caderno, organização de material | OneNote (orientação — ver limites) |
   | banco de dados, consultas, formulários | Access (orientação — ver limites) |

5. **Normas ABNT aplicáveis** — camada [standards/abnt/](standards/abnt/README.md).
   Documentos formais seguem NBR 14724/6023/10520/6024/6027/6028; em slides e
   planilhas, a ABNT rege o **conteúdo citado** (citações, referências, fontes),
   não o visual.
6. **Orientações da escola** — camada [standards/school/](standards/school/README.md),
   sempre combinadas com a ABNT.
7. **Design** — camada [design/](design/README.md) do aplicativo escolhido.

Fluxos prontos (entrada → saída) em [workflows/](workflows/README.md):

- PDF → trabalho DOCX: [workflows/pdf-para-trabalho.md](workflows/pdf-para-trabalho.md)
- PDF → apresentação PPTX: [workflows/pdf-para-apresentacao.md](workflows/pdf-para-apresentacao.md)
- Documento → apresentação: [workflows/documento-para-apresentacao.md](workflows/documento-para-apresentacao.md)
- Dados → planilha: [workflows/dados-para-planilha.md](workflows/dados-para-planilha.md)
- Trabalho ABNT do zero: [workflows/trabalho-abnt.md](workflows/trabalho-abnt.md)
- Apresentação escolar do zero: [workflows/apresentacao-escolar.md](workflows/apresentacao-escolar.md)

## 2. Camadas: ABNT × escola

- **ABNT** = normas técnicas (o que a NBR exige). **Escola** = orientações da
  instituição (flexíveis). São camadas distintas e simultâneas: aplique as duas.
- Conflito aparente: em **documentos formais**, a ABNT prevalece; em
  **apresentações**, a escola/design prevalece no **visual** e a ABNT no
  **conteúdo citado**. Sempre avise o usuário quando arbitrar um conflito.
- Nunca invente número de NBR, regra, formato ou requisito. Na dúvida entre
  edições de norma, diga explicitamente qual edição a fonte consultada cita e
  recomende confirmar na NBR vigente ou no manual da instituição.

## 3. Delegação operacional (skills oficiais)

A manipulação real de arquivos (criar, ler, editar DOCX/PDF/PPTX/XLSX) é feita
**exclusivamente pelas skills oficiais da Anthropic** (`docx`, `pdf`, `pptx`,
`xlsx`), que acompanham o Claude. A `abnt-skill` decide **como** o material
deve ser estruturado, formatado e apresentado; nunca reimplementa OOXML,
fórmulas ou extração de PDF.

Procedimento obrigatório:

1. Leia [applications/office-oficial.md](applications/office-oficial.md) para
   nomes reais, capacidades e limites das skills oficiais.
2. Verifique disponibilidade (menu `/skills` ou tentativa de uso). Se alguma
   skill oficial estiver ausente, siga o fallback documentado lá (modo
   orientado + entrega intermediária em Markdown/TXT) e informe o usuário —
   nunca simule sucesso na manipulação de um arquivo que você não manipulou.
3. Ao delegar, transmita à skill oficial as especificações decididas aqui
   (estrutura, estilos, paleta de até 3 cores, tipografia, margens ABNT,
   textos de atribuição de fontes).

## 4. Padrões inegociáveis de entrega

- **Slides**: texto corrido em **20–25 pt** (faixa desejável), **30 pt = máximo
  recomendado**. Nunca reduza a letra para caber texto demais — corte ou
  reorganize o conteúdo. Referência flexível 10-20-30 (≈10 slides, ≈20 min),
  podendo chegar a ≈20 slides quando necessário.
- **Documentos**: formatação NBR 14724
  ([standards/abnt/formatacao.md](standards/abnt/formatacao.md)).
- **Composição**: simples, limpa, centralizada, hierarquia clara, muito espaço
  livre. Nada de assimetria "moderna" gratuita ou informação jogada nas laterais.
- **Proibido inventar**: sem setas/caixas/linhas/ícones/formas decorativas, sem
  textos de enchimento, sem estatísticas, exemplos ou fatos inventados.
- **Paleta**: no máximo **3 cores** (neutro + cor de títulos + destaque com
  moderação).
- **Visuais úteis**: prefira infográfico, diagramas, gráficos e imagens com
  relação direta com o conteúdo; prefira imagem real (produto, marca, local,
  foto, captura de tela) a imagem gerada por IA.
- **Fontes (origem da informação)**: todo material externo — texto, dados,
  imagem, gráfico, tabela, conceito — recebe atribuição discreta e legível
  (`Fonte: ...`) e, quando apropriado, referências completas no fim. Nunca
  remova créditos existentes; respeite licenças.

## 5. Recursos internos (carregue sob demanda)

| Quando | Carregue |
|---|---|
| Formatação ABNT de documentos | [standards/abnt/](standards/abnt/README.md) |
| Regras da escola (documentos/apresentações) | [standards/school/](standards/school/README.md) |
| Word / PowerPoint / Excel / Outlook / OneNote / Access | [applications/](applications/README.md) |
| Design de documentos / apresentações / planilhas | [design/](design/README.md) |
| PDF / DOCX / XLSX / PPTX / RTF / CSV / TXT | [formats/](formats/README.md) |
| Integração com as skills oficiais | [applications/office-oficial.md](applications/office-oficial.md) |
| Checklist final de qualidade | [assets/checklists/entrega.md](assets/checklists/entrega.md) |

Mantenha esta página como roteador: leia um módulo somente quando a tarefa
exigir, e leia o checklist de entrega antes de finalizar qualquer artefato.

## 6. Limites conhecidos

- **Outlook, OneNote e Access não são cobertos pelas skills oficiais**
  (só existem `docx`, `pdf`, `pptx`, `xlsx`): para eles, a skill entrega
  roteiro orientado + conteúdo pronto para colar, nunca manipulação direta.
- **RTF, CSV e TXT** são tratados como formatos genéricos de intercâmbio, sem
  skill oficial dedicada.
- A ABNT não define estética de slides: o visual de apresentações segue as
  camadas escola + design; a ABNT rege citações, referências e fontes.
- Os textos integrais das NBRs são protegidos por direitos autorais; esta skill
  resume regras a partir de guias públicos citados nos módulos e indica quando
  confirmar na norma vigente.

## 7. Exemplos de invocação

- `/abnt Crie um documento baseado neste PDF.`
- `/abnt Faça um PowerPoint baseado neste PDF.`
- `/abnt Transforme este documento em uma apresentação.`
- `/abnt Organize estes dados em uma planilha.`
- `/abnt Faça um trabalho acadêmico seguindo ABNT.`
- `/abnt Faça uma apresentação seguindo as orientações da escola.`
