# Instalação da abnt-skill

## Requisito: Claude Code

A skill segue o padrão aberto Agent Skills (`SKILL.md`) e usa recursos do
Claude Code: comando via frontmatter `name`, carregamento automático via
`description`/`when_to_use` e substituição `$ARGUMENTS`.

## Passo 1 — instalar a skill

Escolha **um** dos escopos:

```bash
# A) Pessoal — disponível em todos os seus projetos nesta máquina:
mkdir -p ~/.claude/skills
cp -r /caminho/para/abnt-skill ~/.claude/skills/abnt-skill

# B) Projeto — dentro de um repositório, compartilhada via git:
cd /seu/projeto
mkdir -p .claude/skills
cp -r /caminho/para/abnt-skill .claude/skills/abnt-skill
```

> A pasta instalada **precisa** se chamar `abnt-skill` (é a identidade oficial).
> O comando `/abnt` vem do campo `name: abnt` no `SKILL.md` — mecanismo oficial
> do Claude Code ("name sets the command"; o nome do diretório também invoca,
> por isso `/abnt-skill` funciona como alias).

## Passo 2 — conferir as skills oficiais de Office

Não há nada para declarar: a especificação de skills **não possui campo de
dependência skill→skill** (o campo `dependencies` existe apenas em
`plugin.json`, de plugin para plugin). A integração é por delegação em runtime.

Verifique se as 4 skills oficiais estão ativas:

1. Digite `/skills` no Claude Code e procure `docx`, `pdf`, `pptx`, `xlsx`
   (elas acompanham o Claude; podem aparecer como skills da conta/sincronizadas).
2. Se alguma estiver ausente, ative-a nas configurações de skills da sua conta
   (claude.ai → Features/Skills) ou repositório de referência
   `github.com/anthropics/skills` para estudo.
3. Sem elas, a `abnt-skill` opera em **modo orientado** (ver
   [applications/office-oficial.md](applications/office-oficial.md)): entrega
   conteúdo + roteiro em vez de manipular o arquivo diretamente.

## Passo 3 — validar a instalação

```bash
cd ~/.claude/skills/abnt-skill   # ou .claude/skills/abnt-skill
python3 scripts/validate.py
```

Esperado: `OK` em todas as checagens (frontmatter, limites da especificação,
links internos, tamanho do SKILL.md, lista de NBRs).

## Passo 4 — testar o comando

Reinicie o Claude Code (ou aguarde a detecção de mudanças) e digite:

```text
/abnt Faça um trabalho acadêmico seguindo ABNT sobre <tema>.
```

Protocolo completo de testes em [tests/TESTES.md](tests/TESTES.md).

## Notas de portabilidade

- **Plugin?** Não distribuímos como plugin de propósito: skills de plugin são
  namespaced (`/plugin:skill`), o que impediria o comando simples `/abnt`.
- **claude.ai / Skills API:** o upload exige `name` igual ao nome da pasta e só
  aceita os campos `name, description, license, compatibility, metadata,
  allowed-tools`. Para esse caminho, renomeie a pasta para `abnt` e remova
  `when_to_use` e `argument-hint` do frontmatter (o núcleo funciona igual).
