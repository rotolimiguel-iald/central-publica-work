# -*- coding: utf-8 -*-
"""Varredura ESTÁTICA da pedra (rodada 2, F1.TEMPO), só de leitura.

(1) declarações (theorem/def/noncomputable def/abbrev/structure/instance) × linhas `#print axioms`;
(2) tokens proibidos FORA de comentários: sorry, admit, native_decide, `axiom` como declaração;
(3) a constante da casa: nenhum caractere «β», nenhum literal numérico dela (padrões de conferência);
(4) palavras da régua: a palavra recusada como veredito, «não provou», «pós-dição»;
(5) CADA citação «…» do arquivo procurada nas fontes (com espaços normalizados): diz em que fontes aparece.
Uso: python -I varredura_fonte.py <arquivo.lean> <saida.json>
"""
import hashlib
import json
import re
import sys

FONTES = {
    "operador_12out": r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt",
    "operador_05out_verbo": r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v386\VERBO_operador_05out.txt",
    "operador_07out_nomes": r"C:\IALD\Central de Patentes\work\superposicao_passagem_07out\CUNHAGEM_OPERADOR_07out_nomes_verbatim.txt",
    "preregistro_md": r"C:\IALD\Central de Patentes\work\tempo_santo_12out\1_PREREGISTRO\PREREGISTRO.md",
    "kernel_IALDJones": r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\IALDJones.lean",
    "kernel_BisognanoWichmann": r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\BisognanoWichmann.lean",
    "memoria_regra_dois_regimes": r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\regra-dos-dois-regimes.md",
    "claude_md_global": r"C:\Users\rotol\.claude\CLAUDE.md",
}
OPERADOR = {"operador_12out", "operador_05out_verbo", "operador_07out_nomes"}


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def strip_comments(src):
    out, i, depth, n = [], 0, 0, len(src)
    while i < n:
        if src.startswith("/-", i):
            depth += 1
            i += 2
            continue
        if depth > 0 and src.startswith("-/", i):
            depth -= 1
            i += 2
            continue
        if depth == 0 and src.startswith("--", i):
            j = src.find("\n", i)
            i = n if j < 0 else j
            continue
        if depth == 0:
            out.append(src[i])
        i += 1
    return "".join(out)


def main(path, out):
    raw = open(path, "rb").read()
    src = raw.decode("utf-8")
    code = strip_comments(src)
    res = {"arquivo": path, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
    # (1) declarações × #print axioms
    decls = []
    ns = None
    for line in code.split("\n"):
        m = re.match(r"^namespace\s+(\S+)", line)
        if m:
            ns = m.group(1)
        m = re.match(r"^(?:noncomputable\s+)?(?:protected\s+)?(theorem|lemma|def|abbrev|structure|instance)\s+([^\s:({\[]+)", line)
        if m and ns:
            decls.append(ns + "." + m.group(2))
    prints = re.findall(r"^#print axioms\s+(\S+)", code, re.M)
    res["n_declaracoes"] = len(decls)
    res["n_print_axioms"] = len(prints)
    res["declaracoes_sem_print"] = sorted(set(decls) - set(prints))
    res["prints_sem_declaracao"] = sorted(set(prints) - set(decls))
    res["declaracoes_duplicadas"] = sorted({d for d in decls if decls.count(d) > 1})
    res["n_examples"] = len(re.findall(r"^example\b", code, re.M))
    # (2) tokens proibidos fora de comentários
    res["tokens_proibidos_no_codigo"] = {
        "sorry": len(re.findall(r"\bsorry\b", code)),
        "admit": len(re.findall(r"\badmit\b", code)),
        "native_decide": len(re.findall(r"native_decide", code)),
        "axiom_declaracao": len(re.findall(r"^\s*axiom\s", code, re.M)),
    }
    # (3) a constante da casa
    res["constante"] = {
        "caractere_beta": src.count("\u03b2"),
        "literais_de_conferencia": {p: len(re.findall(p, src)) for p in
                                    [r"0[.,]0120", r"0[.,]01203", r"7[.,]297", r"1[.,]6487", r"0[.,]9759"]},
    }
    # (4) palavras da régua
    res["regua"] = {"CONFIRMED": src.count("CONFIRMED"), "confirmad": src.lower().count("confirmad"),
                    "nao_provou": src.lower().count("não provou"), "pos_dicao": src.lower().count("pós-dição")}
    # (5) citações «…»
    fontes_txt = {}
    for k, p in FONTES.items():
        b = open(p, "rb").read()
        fontes_txt[k] = {"norm": norm(b.decode("utf-8")), "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b),
                         "arquivo": p}
    quotes = re.findall(r"«([^»]*)»", src, re.S)
    qres = []
    for q in quotes:
        nq = norm(q)
        achou = [k for k, v in fontes_txt.items() if nq in v["norm"]]
        qres.append({"citacao": nq, "fontes": achou, "do_operador": bool(set(achou) & OPERADOR),
                     "achada": bool(achou)})
    res["citacoes"] = qres
    res["n_citacoes"] = len(qres)
    res["n_citacoes_nao_achadas"] = sum(1 for x in qres if not x["achada"])
    res["fontes"] = {k: {"arquivo": v["arquivo"], "sha256": v["sha256"], "bytes": v["bytes"]} for k, v in fontes_txt.items()}
    op = open(FONTES["operador_12out"], "rb").read().decode("utf-8")
    res["operador_12out_ocorrencias_de_verbo"] = op.lower().count("verbo")
    ok = (not res["declaracoes_sem_print"] and not res["prints_sem_declaracao"] and not res["declaracoes_duplicadas"]
          and all(v == 0 for v in res["tokens_proibidos_no_codigo"].values())
          and res["constante"]["caractere_beta"] == 0
          and all(v == 0 for v in res["constante"]["literais_de_conferencia"].values())
          and res["regua"]["CONFIRMED"] == 0 and res["regua"]["nao_provou"] == 0 and res["regua"]["pos_dicao"] == 0
          and res["n_citacoes_nao_achadas"] == 0)
    res["varredura_ok"] = ok
    with open(out + ".tmp", "w", encoding="utf-8") as fo:
        json.dump(res, fo, ensure_ascii=False, indent=1)
    import os
    os.replace(out + ".tmp", out)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({k: res[k] for k in ("sha256", "n_declaracoes", "n_print_axioms", "declaracoes_sem_print",
                                          "prints_sem_declaracao", "declaracoes_duplicadas", "n_examples",
                                          "tokens_proibidos_no_codigo", "constante", "regua", "n_citacoes",
                                          "n_citacoes_nao_achadas", "operador_12out_ocorrencias_de_verbo",
                                          "varredura_ok")}, ensure_ascii=False))
    for x in qres:
        print(("OK " if x["achada"] else "NAO") + " | " + ",".join(x["fontes"]) + " | " + x["citacao"][:110])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
