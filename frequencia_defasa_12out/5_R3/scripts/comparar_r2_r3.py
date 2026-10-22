# -*- coding: utf-8 -*-
r"""RODADA 3 — compara r2 e r3 declaracao a declaracao e grava:
  5_R3\TIPOS_R2_VS_R3.json   — para cada uma das 190 declaracoes: hash do tipo em r2 e em r3 (do kernel, via run_cmd),
                               tipo impresso, igual?; e a tabela mantida/renomeada/comentario;
  5_R3\TABELA_R2_R3.md        — a mesma tabela em Markdown;
  5_R3\DIFF_r2_r3.txt         — diff unificado do fonte (r2 -> r3), para leitura humana.
Fontes: 5_R3\logs\tipos_r2_SAIDA.txt, tipos_r3_SAIDA.txt (e, se existirem, valores_r2/valores_r3), as duas pedras e
DECLARACOES_R3.json. Nao escreve fora de 5_R3."""
import os, re, json, hashlib, difflib

R3 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNID = os.path.dirname(R3)
P2 = os.path.join(UNID, "3_KERNEL", "rodada2", "sandbox", "TGLExt", "TheUnitIsTheRank.lean")
P3 = os.path.join(R3, "sandbox", "TGLExt", "TheUnitIsTheRank.lean")
NS = "TGLExt.TheUnitIsTheRank."
dec = json.load(open(os.path.join(R3, "DECLARACOES_R3.json"), encoding="utf-8"))
pares = [(x["r2"], x["r3"]) for x in dec["declaracoes"]]


def ler_decl(tag):
    out = {}
    p = os.path.join(R3, "logs", tag + "_SAIDA.txt")
    if not os.path.exists(p):
        return None
    for l in open(p, encoding="utf-8", errors="replace").read().split("\n"):
        if l.startswith("DECL\t"):
            _, n, ht, hv, tipo = l.split("\t", 4)
            out[n[len(NS):]] = {"hash_tipo": ht, "hash_valor": hv, "tipo": tipo.strip()}
    return out


t2, t3 = ler_decl("tipos_r2"), ler_decl("tipos_r3")
v2, v3 = ler_decl("valores_r2"), ler_decl("valores_r3")
if t2 is None or t3 is None or len(t2) != 190 or len(t3) != 190:
    raise SystemExit("FALHA VISIVEL: saidas de tipos ausentes ou incompletas")

s2 = open(P2, encoding="utf-8").read()
s3 = open(P3, encoding="utf-8").read()


def docstrings(src):
    """docstring (/-- ... -/) imediatamente anterior a cada `theorem X`/`def X`; '' se nao ha."""
    out = {}
    for m in re.finditer(r"^(?:theorem|def|noncomputable def) ([A-Za-z0-9_']+)", src, flags=re.M):
        nome, pos = m.group(1), m.start()
        fim = src.rfind("-/", 0, pos)
        entre = src[fim + 2:pos] if fim >= 0 else "x"
        if fim >= 0 and entre.strip() == "":
            ini = src.rfind("/--", 0, fim)
            if ini >= 0 and src.rfind("-/", 0, fim) <= ini:
                out[nome] = src[ini:fim + 2]
                continue
        out[nome] = ""
    return out


d2, d3 = docstrings(s2), docstrings(s3)
tabela, n_ren, n_com, n_man, tipos_iguais, valores_iguais = [], 0, 0, 0, 0, 0
for a, b in pares:
    ti = t2[a]["hash_tipo"] == t3[b]["hash_tipo"] and t2[a]["tipo"] == t3[b]["tipo"]
    tipos_iguais += ti
    vi = None
    if v2 and v3 and a in v2 and b in v3:
        vi = v2[a]["hash_valor"] == v3[b]["hash_valor"]
        valores_iguais += bool(vi)
    doc_mudou = d2.get(a, "") != d3.get(b, "")
    if a != b:
        cat = "RENOMEADA"; n_ren += 1
    elif doc_mudou:
        cat = "COMENTARIO"; n_com += 1
    else:
        cat = "MANTIDA"; n_man += 1
    tabela.append({"r2": a, "r3": b, "categoria": cat, "tipo_igual": ti, "hash_tipo_r2": t2[a]["hash_tipo"],
                   "hash_tipo_r3": t3[b]["hash_tipo"], "valor_igual": vi,
                   "hash_valor_r2": (v2 or {}).get(a, {}).get("hash_valor"),
                   "hash_valor_r3": (v3 or {}).get(b, {}).get("hash_valor"),
                   "docstring_mudou": doc_mudou, "tipo": t3[b]["tipo"]})

# os nomes das tres renomeadas nao aparecem em nenhum tipo (logo os hashes sao comparaveis sem traducao)
ren = [(a, b) for a, b in pares if a != b]
aparece = {a: [n for n, r in t2.items() if re.search(r"\b" + re.escape(a) + r"\b", r["tipo"])] for a, _ in ren}

diff = list(difflib.unified_diff(s2.split("\n"), s3.split("\n"), fromfile="r2 TheUnitIsTheRank.lean (3195ef8f0766384c)",
                                 tofile="r3 TheUnitIsTheRank.lean", lineterm="", n=2))
with open(os.path.join(R3, "DIFF_r2_r3.txt"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(diff) + "\n")

out = {
    "documento": "TIPOS r2 vs r3, declaracao a declaracao (RODADA 3)",
    "pedra_r2_sha256": hashlib.sha256(open(P2, "rb").read()).hexdigest(),
    "pedra_r3_sha256": hashlib.sha256(open(P3, "rb").read()).hexdigest(),
    "n": len(tabela), "tipos_iguais": tipos_iguais, "valores_comparados": bool(v2 and v3), "valores_iguais": valores_iguais,
    "valores_diferentes": [x["r3"] for x in tabela if x["valor_igual"] is False],
    "MANTIDA": n_man, "COMENTARIO": n_com, "RENOMEADA": n_ren,
    "renomeadas": [{"de": a, "para": b, "nome_antigo_aparece_em_algum_tipo_de_r2": aparece[a]} for a, b in ren],
    "todas_as_declaracoes_com_tipo_identico": tipos_iguais == len(tabela),
    "diff_linhas": len(diff),
    "tabela": tabela,
}
with open(os.path.join(R3, "TIPOS_R2_VS_R3.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)

L = ["# TABELA r2 → r3, declaração a declaração (RODADA 3 — TheUnitIsTheRank — 13/10)", "",
     "Tipo lido do kernel (`run_cmd`, `Expr.hash` estrutural + `ppExpr`) nos dois sandboxes; VALOR = hash do termo de "
     "prova/definição (variante thmInfo/defnInfo), quando medido. Categorias: MANTIDA (nome e docstring iguais), "
     "COMENTARIO (só a docstring mudou), RENOMEADA (o identificador mudou; o tipo não).", "",
     "| # | r2 | r3 | categoria | tipo igual | valor igual |", "|---|---|---|---|---|---|"]
for i, x in enumerate(tabela, 1):
    L.append("| %d | `%s` | `%s` | %s | %s | %s |" % (i, x["r2"], x["r3"], x["categoria"], "sim" if x["tipo_igual"] else "NÃO",
                                                   {True: "sim", False: "NÃO", None: "—"}[x["valor_igual"]]))
L += ["", "Totais: MANTIDA %d · COMENTARIO %d · RENOMEADA %d · tipos iguais %d/%d · valores iguais %d/%d" %
      (n_man, n_com, n_ren, tipos_iguais, len(tabela), valores_iguais, len(tabela) if (v2 and v3) else 0)]
with open(os.path.join(R3, "TABELA_R2_R3.md"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(L) + "\n")
print(json.dumps({k: out[k] for k in out if k != "tabela"}, ensure_ascii=False, indent=1))
