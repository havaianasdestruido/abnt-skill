# Access — modo orientado (sem skill oficial)

**Quando usar:** bancos de dados simples, tabelas, consultas, formulários,
relatórios.

Não existe skill oficial para Access: este módulo **não manipula** `.accdb`.
Entrega modelagem + roteiro (e sugere Excel quando o volume cabe em planilha).

## O que a abnt-skill entrega

1. **Modelagem mínima:** tabelas, chaves primárias, relacionamentos e tipos de
   dados descritos em texto + diagrama textual.
2. **Dicionário de dados:** cada campo com descrição, tipo, obrigatoriedade e
   exemplo — serve de documentação do trabalho.
3. **Consultas em SQL padrão** com explicação linha a linha, prontas para
   adaptar no Access; formulários/relatórios descritos campo a campo.
4. **Critério Excel × Access:** até poucas dezenas de milhares de linhas sem
   multiusuário → prefira [excel/](../excel/README.md); acima disso ou com
   integridade relacional → Access, observado o limite de **2 GB por arquivo
   .accdb** (especificações do Access). Para volumes que excedem esse limite,
   recomende particionar em múltiplos back-ends vinculados ou migrar para um
   SGBD dedicado (p.ex. SQL Server/PostgreSQL) em vez de um único .accdb.

Indique os passos manuais no Access — nunca afirme ter criado o banco.
