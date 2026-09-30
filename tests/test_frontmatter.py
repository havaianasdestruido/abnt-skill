#!/usr/bin/env python3
"""Testes de regressao do frontmatter (stdlib-only, sem dependencias).

Cobre o que o parser intencionalmente simples de scripts/validate.py aceita
(valores em linha unica com/sem aspas simples/duplas, mapa 'metadata',
colchetes balanceados como em "[tarefa: ...]") e o que ele rejeita com erro
explicito (sem fechamento '---', linha sem dois-pontos, sequencia nao
fechada, escalar de bloco multilinha, continuacao fora de 'metadata').

Uso: python3 tests/test_frontmatter.py
Saida: lista de PASS/FAIL por caso; exit code 0 se tudo OK.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from validate import parse_frontmatter, validate_field_types

failures = []


def expect_ok(label, doc, expected):
    data, err = parse_frontmatter(doc)
    ok = err == "" and data == expected and validate_field_types(data) == ""
    print(f"[{'PASS' if ok else 'FAIL'}] aceita: {label}" + ("" if ok else f" -- data={data!r} err={err!r}"))
    if not ok:
        failures.append(label)


def expect_err(label, doc):
    data, err = parse_frontmatter(doc)
    ok = data is None and err != ""
    print(f"[{'PASS' if ok else 'FAIL'}] rejeita: {label}" + ("" if ok else f" -- data={data!r} err={err!r}"))
    if not ok:
        failures.append(label)


def main():
    ok_base = "---\nname: abnt\ndescription: Produz trabalhos\n---\n\n# corpo\n"
    expect_ok("basico sem aspas", ok_base, {"name": "abnt", "description": "Produz trabalhos"})
    expect_ok("aspas duplas", "---\nname: \"abnt\"\n---\n\nx\n", {"name": "abnt"})
    expect_ok("aspas simples", "---\nname: 'abnt'\n---\n\nx\n", {"name": "abnt"})
    expect_ok("valor com dois-pontos", "---\nname: a: b\n---\n\nx\n", {"name": "a: b"})
    expect_ok(
        "colchetes balanceados",
        "---\nargument-hint: [tarefa: documento | slide]\n---\n\nx\n",
        {"argument-hint": "[tarefa: documento | slide]"},
    )
    expect_ok(
        "mapa metadata",
        "---\nname: abnt\nmetadata:\n  identidade: abnt-skill\n---\n\nx\n",
        {"name": "abnt", "metadata": {"identidade": "abnt-skill"}},
    )

    expect_err("sem fechamento", "---\nname: abnt\n\n# corpo\n")
    expect_err("linha sem dois-pontos", "---\nname abnt\n---\n\nx\n")
    expect_err("sequencia nao fechada", "---\nname: [a, b\n---\n\nx\n")
    expect_err("mapa nao fechado", "---\nname: {a: b\n---\n\nx\n")
    expect_err("bloco literal multilinha", "---\ndescription: |\n  linha 1\n  linha 2\n---\n\nx\n")
    expect_err("bloco dobrado multilinha", "---\ndescription: >\n  linha 1\n---\n\nx\n")
    expect_err("indentada fora de metadata", "---\nname: abnt\n  solta: x\n---\n\nx\n")
    expect_err("metadata com valor inline", "---\nmetadata: foo\n---\n\nx\n")

    # Tipos decodificados: dicionario forjado com tipo errado deve falhar.
    type_err = validate_field_types({"name": ["abnt"]})
    ok = type_err != ""
    print(f"[{'PASS' if ok else 'FAIL'}] rejeita: tipo nao-texto em campo")
    if not ok:
        failures.append("tipo nao-texto em campo")

    print()
    if failures:
        print(f"RESULTADO: {len(failures)} FALHA(S): {', '.join(failures)}")
        return 1
    print("RESULTADO: OK -- todos os casos passaram.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
