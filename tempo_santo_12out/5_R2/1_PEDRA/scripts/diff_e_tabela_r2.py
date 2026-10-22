# -*- coding: utf-8 -*-
"""DIFF.patch R1 -> R2 (unified, por linhas) e a TABELA declaracao a declaracao (mantida / renomeada / removida /
nova), lidas das DUAS fontes por regex. Classificacao:
  - renomeada: pares da lista E5 (E5.06, E5.07, E5.08); o tipo identico e conferido a parte, em Lean
    (AuditTiposR2.lean, type_of%);
  - removida: nome presente so na R1;
  - nova: nome presente so na R2 e que nao e alvo de renome;
  - mantida: mesmo nome nas duas; sub-rotulo (texto identico) ou (texto alterado: docstring/prova/tipo), pelo sha16 do
    bloco (da docstring `/--` imediatamente anterior ate a linha antes da proxima declaracao). Os reforcos de tipo
    (E5.11, E5.12) e a troca de `True` por enunciado (E5.09) sao marcados a parte.
`example` (anonimo) conta-se por arquivo. Nada e alterado fora de 5_R2/1_PEDRA.
Uso: python -I -X utf8 diff_e_tabela_r2.py <R1.lean> <R2.lean> <saida_dir>
"""
import difflib
import hashlib
import json
import os
import re
import sys

DECL = re.compile(r"^(?:noncomputable\s+)?(theorem|def|abbrev|instance|structure|lemma|example)\b\s*([^\s:({\[]*)", re.M)
RENOMES = {  # R1 -> R2 (ADENDO_R2 §c)
    "time_is_the_modular_flow": ("modular_flow_is_a_kms_group", "E5.06"),
    "the_time_has_no_rank": ("the_time_is_not_a_post", "E5.07"),
    "probe_the_time_has_no_rank": ("probe_the_time_is_not_a_post", "E5.07"),
    "optical_attractor_is_the_absolute_one": ("half_identity_is_absoluteRho_two", "E5.08"),
    "optical_attractor_clock_stops": ("half_identity_clock_stops", "E5.08"),
}
REFORCOS = {"purityR_modular": "E5.11 (hipotese `_hd` removida; tipo mais forte)",
            "clock_reads_modulo_period": "E5.12 (hipotese `κ ≠ 0` removida; tipo mais forte)",
            "the_two_regimes_of_time": "E5.12 (conjunto 8 para todo κ; tipo mais forte)",
            "probe_bounded_spectral_translation": "E5.09 (de `True` para o enunciado da instancia)"}


def sha16(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def blocos(txt):
    """nome -> (linha, kind, sha16 do bloco). Bloco = docstring imediatamente anterior + declaracao ate a proxima."""
    linhas = txt.split("\n")
    marcas = []
    for m in DECL.finditer(txt):
        ln = txt.count("\n", 0, m.start()) + 1
        marcas.append((ln, m.group(1), m.group(2)))
    out = {}
    examples = []
    for idx, (ln, kind, name) in enumerate(marcas):
        fim = marcas[idx + 1][0] - 1 if idx + 1 < len(marcas) else len(linhas)
        ini = ln
        # docstring imediatamente anterior (e set_option ... in)
        j = ln - 2
        while j >= 0 and linhas[j].strip() == "":
            j -= 1
        if j >= 0 and linhas[j].rstrip().endswith("-/"):
            k = j
            while k >= 0 and not linhas[k].lstrip().startswith("/--"):
                k -= 1
            if k >= 0:
                ini = k + 1
        if ini - 2 >= 0 and linhas[ini - 2].strip().startswith("set_option") and linhas[ini - 2].strip().endswith(" in"):
            ini -= 1
        bloco = "\n".join(linhas[ini - 1:fim]).rstrip()
        # o bloco nao pode engolir a docstring da proxima declaracao
        if idx + 1 < len(marcas):
            nxt = marcas[idx + 1][0]
            corte = nxt - 1
            jj = nxt - 2
            while jj >= 0 and linhas[jj].strip() == "":
                jj -= 1
            if jj >= 0 and linhas[jj].rstrip().endswith("-/"):
                kk = jj
                while kk >= 0 and not linhas[kk].lstrip().startswith("/--"):
                    kk -= 1
                if kk >= 0:
                    corte = kk
            if ini - 2 >= 0 and linhas[nxt - 2].strip().startswith("set_option") and linhas[nxt - 2].strip().endswith(" in"):
                corte = min(corte, nxt - 2)
            bloco = "\n".join(linhas[ini - 1:corte]).rstrip()
        if kind == "example" or not name:
            examples.append({"linha": ln, "sha16": sha16(bloco)})
        else:
            out[name] = {"linha": ln, "kind": kind, "sha16_bloco": sha16(bloco)}
    return out, examples


def main(r1, r2, outdir):
    b1 = open(r1, "rb").read()
    b2 = open(r2, "rb").read()
    t1 = b1.decode("utf-8")
    t2 = b2.decode("utf-8")
    diff = list(difflib.unified_diff(t1.splitlines(True), t2.splitlines(True),
                                     fromfile="R1/3_KERNEL/sandbox/TheTimeHasNoRank.lean",
                                     tofile="R2/5_R2/1_PEDRA/sandbox/TheTimeIsNotAPost.lean", n=3))
    patch = "".join(diff)
    with open(os.path.join(outdir, "DIFF.patch.tmp"), "wb") as f:
        f.write(patch.encode("utf-8"))
    os.replace(os.path.join(outdir, "DIFF.patch.tmp"), os.path.join(outdir, "DIFF.patch"))
    d1, ex1 = blocos(t1)
    d2, ex2 = blocos(t2)
    alvos = {v[0] for v in RENOMES.values()}
    tabela = []
    for n, info in d1.items():
        if n in RENOMES:
            novo, item = RENOMES[n]
            tabela.append({"R1": n, "R2": novo, "classe": "renomeada", "item_E5": item, "kind": info["kind"],
                           "linha_R1": info["linha"], "linha_R2": d2.get(novo, {}).get("linha"),
                           "tipo": "identico (conferido em Lean: AuditTiposR2)"})
        elif n in d2:
            igual = info["sha16_bloco"] == d2[n]["sha16_bloco"]
            e = {"R1": n, "R2": n, "classe": "mantida", "kind": info["kind"], "linha_R1": info["linha"],
                 "linha_R2": d2[n]["linha"], "texto": "identico" if igual else "alterado (docstring/prova/tipo)"}
            if n in REFORCOS:
                e["classe"] = "mantida (tipo reforcado)"
                e["item_E5"] = REFORCOS[n]
            tabela.append(e)
        else:
            tabela.append({"R1": n, "R2": None, "classe": "removida", "kind": info["kind"], "linha_R1": info["linha"],
                           "item_E5": "E5.10" if n == "the_absolute_one_has_no_clock" else "?"})
    for n, info in d2.items():
        if n not in d1 and n not in alvos:
            tabela.append({"R1": None, "R2": n, "classe": "nova", "kind": info["kind"], "linha_R2": info["linha"]})
    from collections import Counter
    cont = Counter(e["classe"] for e in tabela)
    res = {"R1": {"arquivo": r1, "sha256": hashlib.sha256(b1).hexdigest(), "bytes": len(b1), "n_declaracoes_nomeadas": len(d1),
                  "n_examples": len(ex1)},
           "R2": {"arquivo": r2, "sha256": hashlib.sha256(b2).hexdigest(), "bytes": len(b2), "n_declaracoes_nomeadas": len(d2),
                  "n_examples": len(ex2)},
           "diff": {"arquivo": os.path.join(outdir, "DIFF.patch"), "sha256": hashlib.sha256(patch.encode("utf-8")).hexdigest(),
                    "n_linhas_removidas": sum(1 for l in diff if l.startswith("-") and not l.startswith("---")),
                    "n_linhas_acrescentadas": sum(1 for l in diff if l.startswith("+") and not l.startswith("+++"))},
           "contagem_por_classe": dict(cont),
           "nota_contagem": "declaracoes nomeadas por regex (theorem/def/abbrev/instance/structure); `example` anonimo contado a parte; "
                            "a contagem de TEOREMAS do relatorio exclui re-exportacoes, sondas, controles, definicoes e desdobramentos (E5.14)",
           "tabela": tabela}
    with open(os.path.join(outdir, "TABELA_DECLARACOES_R2.json.tmp"), "wb") as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=1).encode("utf-8"))
    os.replace(os.path.join(outdir, "TABELA_DECLARACOES_R2.json.tmp"), os.path.join(outdir, "TABELA_DECLARACOES_R2.json"))
    # markdown
    md = ["# Tabela declaração a declaração — pedra R1 (`TheTimeHasNoRank.lean`) → pedra R2 (`TheTimeIsNotAPost.lean`)", "",
          "R1 sha256 `%s` (%d B); R2 sha256 `%s` (%d B). Contagem: %s. `example` anónimos: R1 %d, R2 %d." % (
              res["R1"]["sha256"][:16] + "…", len(b1), res["R2"]["sha256"][:16] + "…", len(b2),
              ", ".join("%s %d" % kv for kv in sorted(cont.items())), len(ex1), len(ex2)), "",
          "| classe | R1 | R2 | kind | l.R1 | l.R2 | nota |", "|---|---|---|---|---|---|---|"]
    ordem = {"renomeada": 0, "removida": 1, "nova": 2, "mantida (tipo reforcado)": 3, "mantida": 4}
    for e in sorted(tabela, key=lambda e: (ordem.get(e["classe"], 9), e.get("linha_R1") or 10 ** 6, e.get("linha_R2") or 10 ** 6)):
        nota = e.get("item_E5") or e.get("texto") or e.get("tipo") or ""
        md.append("| %s | %s | %s | %s | %s | %s | %s |" % (e["classe"], "`%s`" % e["R1"] if e["R1"] else "—",
                                                       "`%s`" % e["R2"] if e["R2"] else "—", e.get("kind", ""),
                                                       e.get("linha_R1") or "—", e.get("linha_R2") or "—", nota))
    with open(os.path.join(outdir, "TABELA_DECLARACOES_R2.md.tmp"), "wb") as f:
        f.write("\n".join(md).encode("utf-8") + b"\n")
    os.replace(os.path.join(outdir, "TABELA_DECLARACOES_R2.md.tmp"), os.path.join(outdir, "TABELA_DECLARACOES_R2.md"))
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({k: v for k, v in res.items() if k != "tabela"}, ensure_ascii=False, indent=1))
    for e in tabela:
        if e["classe"] != "mantida" or e.get("texto") != "identico":
            print(e["classe"], "|", e["R1"], "->", e["R2"], "|", e.get("item_E5", e.get("texto", "")))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
