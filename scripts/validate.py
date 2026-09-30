#!/usr/bin/env python3
"""Validador estatico da abnt-skill.

Checa, sem inventar mecanismos:
 1. Frontmatter do SKILL.md (YAML valido, campos conhecidos, limites da spec:
    name 1-64 kebab-case sem hifens consecutivos, description 1-1024,
    compatibility <=500, sem palavras reservadas 'anthropic'/'claude' no name).
 2. SKILL.md com menos de 500 linhas (recomendacao oficial).
 3. Todos os links relativos internos resolvendo para arquivos existentes.
 4. Identidade unica: nenhuma mencao a skills principais concorrentes.
 5. NBRs citadas restritas a lista pesquisada (anti-invencao de normas).
 6. Separacao operacional: nenhum script local manipula formatos Office de
    forma direta (a operacao e das skills oficiais).
 7. Presenca dos modulos/documentos obrigatorios.

Uso: python3 scripts/validate.py
Saida: lista de PASS/FAIL por checagem; exit code 0 se tudo OK.

Nota: a checagem de identidade varre o conteudo da skill, excluindo a
infraestrutura de teste (tests/).

Nota sobre o parser de frontmatter: intencionalmente simples e stdlib-only
(sem PyYAML), adequado ao frontmatter pequeno e controlado desta skill.
Aceita escalares em linha unica (com/sem aspas simples/duplas) e o mapa
'metadata'. Falha explicitamente (fail-closed) diante de construtos nao
suportados — sequencias/mapas desbalanceados, escalares de bloco (|, >),
continuacoes indentadas fora de 'metadata' — em vez de interpretar errado.
Regressoes em tests/test_frontmatter.py.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def strip_quotes(value):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def brackets_balanced(value):
    return value.count("[") == value.count("]") and value.count("{") == value.count("}")


def parse_frontmatter(text):
    if not text.startswith("---"):
        return None, "SKILL.md nao comeca com '---'"
    end = text.find("\n---", 3)
    if end == -1:
        return None, "frontmatter sem fechamento '---'"
    raw = text[3:end].strip()
    data, current_key = {}, None
    try:
        for line in raw.splitlines():
            if not line.strip() or line.strip().startswith("#"):
                continue
            if re.match(r"^\s", line):
                if current_key != "metadata":
                    return None, f"continuacao indentada fora de 'metadata': {line!r}"
                k, sep, v = line.strip().partition(":")
                if not sep:
                    return None, f"linha invalida no frontmatter: {line!r}"
                data[current_key][k.strip()] = strip_quotes(v.strip())
                continue
            k, sep, v = line.partition(":")
            if not sep:
                return None, f"linha invalida no frontmatter: {line!r}"
            k, v = k.strip(), v.strip()
            if v[:1] in ("|", ">"):
                return None, (
                    f"escalar de bloco nao suportado em {k!r}: use valor escalar "
                    f"em linha unica"
                )
            if not brackets_balanced(v):
                return None, (
                    f"sequencia/mapa desbalanceado em {k!r}: {v!r} "
                    f"(sequencias nao fechadas nao sao aceitas)"
                )
            v = strip_quotes(v)
            if k == "metadata":
                if v:
                    return None, f"'metadata' exige mapa indentado, nao valor: {v!r}"
                data[k] = {}
                current_key = k
            else:
                data[k] = v
                current_key = None
    except Exception as e:  # noqa: BLE001 - validador simples
        return None, f"erro de parse: {e}"
    return data, ""


def validate_field_types(fm):
    for key, value in fm.items():
        if key == "metadata":
            if not isinstance(value, dict):
                return f"'metadata' deve ser um mapa, nao {type(value).__name__}"
            for sub, subval in value.items():
                if not isinstance(subval, str):
                    return f"metadata.{sub} deve ser texto, nao {type(subval).__name__}"
        elif not isinstance(value, str):
            return f"campo {key!r} deve ser texto, nao {type(value).__name__}"
    return ""


def build_office_patterns():
    # Fragmentos montados em runtime para este proprio arquivo nao conter os
    # literais procurados (evita auto-deteccao). Cada tupla forma um padrao.
    parts = [
        ("zip", "file"),
        ("oo", "xml"),
        ("python-", "docx"),
        ("docx", ".Document"),
        ("open", "pyxl"),
        ("pptx", ".Presentation"),
        ("Py", "PDF2"),
        ("py", "pdf"),
        ("fi", "tz."),
        ("libre", "office"),
        ("soffice", ""),
    ]
    return ["".join(p) for p in parts]


def file_has_office_usage(path):
    patterns = build_office_patterns()
    hits = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = line.strip()
        # Ignora as linhas que definem os proprios fragmentos de busca.
        if re.match(r'^\(\s*"[a-zA-Z.]+"\s*,\s*"[a-zA-Z.]*"\s*\)\s*,?\s*(#.*)?$', stripped):
            continue
        if "Fragmentos montados em runtime" in line:
            continue
        for pat in patterns:
            if pat and pat in line:
                hits.append(f"{path.name}:{i}:{pat}")
    return hits


def main():
    skill = ROOT / "SKILL.md"
    text = skill.read_text(encoding="utf-8")
    fm, err = parse_frontmatter(text)
    check("frontmatter parseavel", fm is not None, err)

    if fm is not None:
        type_err = validate_field_types(fm)
        check("tipos do frontmatter validos", not type_err, type_err)
        known = {"name", "description", "when_to_use", "argument-hint", "license",
                 "compatibility", "metadata", "allowed-tools", "user-invocable",
                 "disable-model-invocation"}
        unknown = [k for k in fm if k not in known]
        check("campos do frontmatter conhecidos", not unknown, f"desconhecidos: {unknown}")

        name = fm.get("name", "")
        check("name presente e <=64 chars", 1 <= len(name) <= 64, repr(name))
        check("name em kebab-case", bool(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name)), repr(name))
        check("name sem hifens consecutivos", "--" not in name)
        check("name sem palavras reservadas", "anthropic" not in name and "claude" not in name)
        check("name == 'abnt' (comando /abnt)", name == "abnt", repr(name))

        desc = fm.get("description", "")
        check("description 1-1024 chars", 1 <= len(desc) <= 1024, f"{len(desc)} chars")
        combo = len(desc) + len(fm.get("when_to_use", ""))
        check("description+when_to_use <=1536 (listagem)", combo <= 1536, f"{combo} chars")
        blob = (desc + " " + fm.get("when_to_use", "")).lower()
        for kw in ["abnt", "trabalho", "apresenta", "planilha", "word", "powerpoint", "excel"]:
            check(f"roteamento menciona '{kw}'", kw in blob)

        compat = fm.get("compatibility", "")
        check("compatibility <=500 chars", len(compat) <= 500, f"{len(compat)} chars")
        check("metadata.identidade == abnt-skill",
              isinstance(fm.get("metadata"), dict) and fm["metadata"].get("identidade") == "abnt-skill")
        check("corpo usa $ARGUMENTS", "$ARGUMENTS" in text)

    lines = text.splitlines()
    check("SKILL.md <500 linhas", len(lines) < 500, f"{len(lines)} linhas")

    # Links relativos internos
    link_re = re.compile(r"\[[^\]]*\]\(([^)#]+)(?:#[^)]*)?\)")
    broken = []
    md_files = sorted(ROOT.rglob("*.md"))
    for md in md_files:
        for m in link_re.finditer(md.read_text(encoding="utf-8")):
            href = m.group(1).strip()
            if not href or href.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = (md.parent / href).resolve()
            try:
                target.relative_to(ROOT.resolve())
            except ValueError:
                broken.append(f"{md.relative_to(ROOT)} -> {href} (fora da raiz)")
                continue
            if not target.exists():
                broken.append(f"{md.relative_to(ROOT)} -> {href}")
    check("links internos resolvem", not broken, "; ".join(broken[:5]))

    # Identidade unica (exclui infra de teste, que cita os termos p/ documentar)
    rivals = ["office-skills", "abnt-office", "school-office", "academic-office"]
    hits = []
    for md in md_files:
        if md.relative_to(ROOT).parts[0] in ("tests", "scripts"):
            continue
        content = md.read_text(encoding="utf-8").lower()
        for r in rivals:
            if r in content:
                hits.append(f"{md.relative_to(ROOT)}: {r}")
    check("sem skills principais concorrentes", not hits, "; ".join(hits[:5]))

    # Anti-invencao de NBRs
    allowed_nbrs = {"14724", "10520", "6023", "6024", "6027", "6028", "6022", "15287", "12225", "6034"}
    bad_nbrs = []
    for md in md_files:
        for m in re.finditer(r"NBR\s*(\d{4,5})", md.read_text(encoding="utf-8")):
            if m.group(1) not in allowed_nbrs:
                bad_nbrs.append(f"{md.relative_to(ROOT)}: NBR {m.group(1)}")
    check("NBRs citadas restritas a lista pesquisada", not bad_nbrs, "; ".join(bad_nbrs[:5]))

    # Separacao operacional: scripts locais nao manipulam Office
    op_hits = []
    for py in sorted((ROOT / "scripts").glob("*.py")):
        op_hits.extend(file_has_office_usage(py))
    check("scripts sem manipulacao Office (sem duplicacao)", not op_hits, "; ".join(op_hits[:5]))

    # Modulos obrigatorios
    required = [
        "SKILL.md", "README.md", "INSTALL.md", "LICENSE",
        "standards/abnt/formatacao.md", "standards/abnt/citacoes.md",
        "standards/abnt/referencias.md", "standards/abnt/normas.md",
        "standards/abnt/numeracao-sumario-resumo.md", "standards/abnt/artigos-projetos.md",
        "standards/school/documents/README.md", "standards/school/presentations/README.md",
        "applications/office-oficial.md", "applications/word/README.md",
        "applications/powerpoint/README.md", "applications/excel/README.md",
        "applications/outlook/README.md", "applications/onenote/README.md",
        "applications/access/README.md", "design/documents/README.md",
        "design/presentations/README.md", "design/spreadsheets/README.md",
        "formats/pdf/README.md", "formats/docx/README.md", "formats/xlsx/README.md",
        "formats/pptx/README.md", "formats/rtf/README.md", "formats/csv/README.md",
        "formats/txt/README.md", "workflows/pdf-para-trabalho.md",
        "workflows/pdf-para-apresentacao.md", "workflows/documento-para-apresentacao.md",
        "workflows/dados-para-planilha.md", "workflows/trabalho-abnt.md",
        "workflows/apresentacao-escolar.md", "assets/checklists/entrega.md",
        "docs/INTEGRACAO-OFFICE.md", "docs/RELATORIO-FINAL.md", "tests/TESTES.md",
    ]
    missing = [r for r in required if not (ROOT / r).exists()]
    check("modulos obrigatorios presentes", not missing, "; ".join(missing[:8]))

    print()
    if failures:
        print(f"RESULTADO: {len(failures)} FALHA(S): {', '.join(failures)}")
        return 1
    print("RESULTADO: OK -- todas as checagens passaram.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
