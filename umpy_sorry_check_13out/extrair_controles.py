# -*- coding: utf-8 -*-
"""Extrai, SEM executar o um.py, os controles Lean embutidos (literais via ast.literal_eval
das linhas do arquivo) e procura o token sorry fora de comentarios. So leitura do um.py."""
import ast, base64, hashlib, json, lzma, re, sys, zlib
from pathlib import Path

UM = Path(r"C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um.py")
OUT = Path(r"C:/IALD/Central de Patentes/work/umpy_sorry_check_13out")

raw = UM.read_bytes()
sha = hashlib.sha256(raw).hexdigest()
lines = raw.decode("utf-8").splitlines()


def block(name, closer):
    start = None
    for i, l in enumerate(lines):
        if l.startswith(name + " = "):
            start = i
            break
    if start is None:
        raise KeyError(name)
    if lines[start].rstrip().endswith(("]", "}")) and lines[start].count("\n") == 0 and not lines[start].rstrip().endswith(("[", "{")):
        txt = lines[start].split(" = ", 1)[1]
        return ast.literal_eval(txt), start + 1
    j = start + 1
    while not lines[j].startswith(closer):
        j += 1
    txt = "\n".join(lines[start:j + 1]).split(" = ", 1)[1]
    return ast.literal_eval(txt), start + 1


controls, l_ctrl = block("_BENCH_LEAN_CONTROLS", "]")
register, _ = block("_BENCH_CORPUS_REGISTER", "]")
corpus, _ = block("_EMBEDDED_BENCH_CORPUS", "}")
meta, _ = block("_BENCH_ARCHIVE_V361_META", "}")
index, _ = block("_BENCH_ARCHIVE_V361_INDEX", "]")
arch, _ = block("_EMBEDDED_BENCH_ARCHIVE_V361", "]")

reg = {r[0]: r for r in register}
comp = base64.b64decode("".join(arch))
assert hashlib.sha256(comp).hexdigest() == meta["xz_sha256"], "xz sha nao confere"
blob = lzma.decompress(comp)
idx = {r[0]: r for r in index}


def get_bytes(p):
    if p in reg and reg[p][3] == "EMBEDDED":
        d = zlib.decompress(base64.b64decode(corpus[p]))
        ok = len(d) == reg[p][1] and hashlib.sha256(d).hexdigest() == reg[p][2]
        return d, "corpus_embutido", ok
    r = idx[p]
    d = blob[r[1]:r[1] + r[2]]
    ok = len(d) == r[2] and hashlib.sha256(d).hexdigest() == r[3]
    return d, "arquivo_v361", ok


def strip_comments(src):
    # remove comentarios de bloco /- ... -/ (aninhados) e de linha -- ; e strings "..."
    out, i, depth, n = [], 0, 0, len(src)
    while i < n:
        if src.startswith("/-", i):
            depth += 1; i += 2; continue
        if depth and src.startswith("-/", i):
            depth -= 1; i += 2; continue
        if depth:
            out.append("\n" if src[i] == "\n" else " "); i += 1; continue
        if src.startswith("--", i):
            while i < n and src[i] != "\n":
                i += 1
            continue
        if src[i] == '"':
            j = i + 1
            while j < n and src[j] != '"':
                j += 2 if src[j] == "\\" else 1
            out.append('""'); i = j + 1; continue
        out.append(src[i]); i += 1
    return "".join(out)


tok = re.compile(r"(?<![A-Za-z0-9_.'])(sorry|admit|sorryAx)(?![A-Za-z0-9_'])")
axdecl = re.compile(r"^\s*(?:private\s+|protected\s+)?axiom\s", re.M)
rows = []
for c in controls:
    pth, emb, sha_, kind, module, is_dep = c
    d, origem, ok = get_bytes(emb)
    sha_ok = ok and hashlib.sha256(d).hexdigest() == sha_
    src = d.decode("utf-8")
    code = strip_comments(src)
    hits_code = [(code[:m.start()].count("\n") + 1, m.group(1)) for m in tok.finditer(code)]
    hits_raw = len(tok.findall(src))
    rows.append({
        "control": pth, "embedded_as": emb, "kind": kind, "module": module, "is_dep": is_dep,
        "origem": origem, "sha256_ok": sha_ok, "bytes": len(d),
        "sorry_tokens_in_code": hits_code, "sorry_tokens_raw_incl_comments": hits_raw,
        "print_axioms_lines": len(re.findall(r"^\s*#print\s+axioms", src, re.M)),
        "axiom_declarations_in_code": len(axdecl.findall(code)),
        "options_sorry_or_warning": bool(re.search(r"set_option\s+(warningAsError|linter)", code)),
    })

summ = {
    "um_py_sha256": sha, "um_py_sha16": sha[:16], "line_BENCH_LEAN_CONTROLS": l_ctrl,
    "n_controls": len(rows),
    "n_positivo": sum(r["kind"] == "POSITIVO" for r in rows),
    "n_negativo": sum(r["kind"] == "NEGATIVO" for r in rows),
    "all_sha256_ok": all(r["sha256_ok"] for r in rows),
    "positivos_com_sorry_no_codigo": [r["control"] for r in rows if r["kind"] == "POSITIVO" and r["sorry_tokens_in_code"]],
    "negativos_com_sorry_no_codigo": [r["control"] for r in rows if r["kind"] == "NEGATIVO" and r["sorry_tokens_in_code"]],
    "positivos_com_token_so_em_comentario": [r["control"] for r in rows if r["kind"] == "POSITIVO" and not r["sorry_tokens_in_code"] and r["sorry_tokens_raw_incl_comments"]],
    "positivos_com_print_axioms": sum(1 for r in rows if r["kind"] == "POSITIVO" and r["print_axioms_lines"]),
    "positivos_com_declaracao_axiom": [r["control"] for r in rows if r["kind"] == "POSITIVO" and r["axiom_declarations_in_code"]],
    "rows": rows,
}
(OUT / "controles_extraidos.json").write_text(json.dumps(summ, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({k: v for k, v in summ.items() if k != "rows"}, ensure_ascii=False, indent=1))
