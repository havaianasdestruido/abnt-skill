# formats/ — formatos de entrada e saída

Reconhecimento e conversão entre formatos. Quem executa a conversão nos
formatos Office é a skill oficial correspondente.

| Módulo | Papel |
|---|---|
| [pdf/](pdf/README.md) | leitura/extração, referência de conteúdo, saída final não-editável |
| [docx/](docx/README.md) | documentos editáveis (Word) |
| [xlsx/](xlsx/README.md) | planilhas (Excel) |
| [pptx/](pptx/README.md) | apresentações (PowerPoint) |
| [rtf/](rtf/README.md) | texto formatado genérico (intercâmbio; sem abstração de app específico) |
| [csv/](csv/README.md) | dados tabulares brutos → normalizar em XLSX |
| [txt/](txt/README.md) | texto puro/Markdown como intermediário e fallback |

Fluxos completos de conversão em [../workflows/](../workflows/README.md).
