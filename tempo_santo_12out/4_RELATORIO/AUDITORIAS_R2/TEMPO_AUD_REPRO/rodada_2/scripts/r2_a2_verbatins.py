"""Auditor de reproducao F1.TEMPO, rodada 2 -- item (2): os verbatins do pre-registro e da docstring da pedra
batem byte a byte com os arquivos-fonte? Somente leitura. Saida JSON em argv[1].
Parte A: texto do operador (arquivo, segunda parte, 23 frases) e os 14 verbatins_citados (30 excertos por offset).
Parte B: toda citacao entre aspas angulares na pedra da rodada 2 (a pedra declara, l.42, que essas aspas cercam SO
citacao verbatim conferida nos bytes): busca exata (bytes UTF-8) e, se falhar, busca com espacos normalizados,
num conjunto de fontes candidatas; relata onde achou.
"""
import glob, hashlib, json, os, re, sys

LONG = "\\\\?\\"
BASE = r"C:\IALD\Central de Patentes\work\tempo_santo_12out"
PRE = os.path.join(BASE, "1_PREREGISTRO", "PREREGISTRO.json")
PEDRA = os.path.join(BASE, "3_KERNEL", "rodada_2", "sandbox", "TheTimeHasNoRank.lean")
PEDRA_SHA = "a68539d8cf14260da35316b01b3be28e6021f2940f030dea6bc7d5412c58162b"
KER = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel"
MEM = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"


def rb(p):
    with open(LONG + p if not p.startswith(LONG) else p, "rb") as f:
        return f.read()


def sha(b):
    return hashlib.sha256(b).hexdigest()


out = {}
pre = json.loads(rb(PRE).decode("utf-8"))

# ---------- Parte A ----------
t = pre["texto_do_operador"]
ob = rb(t["arquivo"])
A = {"arquivo_sha_ok": sha(ob) == t["sha256"], "arquivo_bytes_ok": len(ob) == t["bytes"], "crlf": ob.count(b"\r\n")}
sp = t["segunda_parte"]
seg = ob[sp["byte_offset"]:sp["byte_offset"] + sp["bytes"]]
A["segunda_parte"] = {"sha_ok": sha(seg) == sp["sha256"], "vai_ate_o_fim": sp["byte_offset"] + sp["bytes"] == len(ob),
                      "comeca_com": seg[:64].decode("utf-8", "replace"),
                      "comeca_certo": seg.decode("utf-8").startswith("O que mais me fascina é a impossibilidade de definição do tempo.")}
fr = []
cobertos = bytearray(len(ob))
for f in t["frases"]:
    s = ob[f["byte_offset"]:f["byte_offset"] + f["bytes"]]
    ok = (sha(s) == f["sha256"]) and (s.decode("utf-8") == f["texto"])
    for i in range(f["byte_offset"], f["byte_offset"] + f["bytes"]):
        cobertos[i] = 1
    fr.append({"id": f["id"], "ok": ok})
fora = bytes(ob[i] for i in range(sp["byte_offset"], len(ob)) if not cobertos[i])
A["frases"] = {"n": len(fr), "todas_ok": all(x["ok"] for x in fr), "falhas": [x for x in fr if not x["ok"]],
               "bytes_da_segunda_parte_fora_das_frases": len(fora), "fora_so_espaco_e_marcacao": fora.decode("utf-8", "replace").strip(" \n*\"“”") == "" or repr(fora.decode("utf-8", "replace"))}
vs = []
for v in pre["verbatins_citados"]:
    b = rb(v["arquivo"])
    rec = {"id": v["id"], "arquivo": v["arquivo"], "sha_registrado": v["sha256"][:16], "sha_agora": sha(b)[:16], "sha_ok": sha(b) == v["sha256"],
           "bytes_registrado": v["bytes"], "bytes_agora": len(b)}
    if not rec["sha_ok"]:
        pref = b[:v["bytes"]]
        rec["prefixo_congelado_confere"] = sha(pref) == v["sha256"]
    exs = []
    for e in v["excertos"]:
        o, n = int(e["byte_offset"]), int(e["bytes"])
        s = b[o:o + n]
        exs.append({"id": e["id"], "ok": (sha(s) == e["sha256"]) and (s.decode("utf-8", "replace") == e["texto"]),
                    "linha_ok": (b[:o].count(b"\n") + 1) == int(e["linha"])})
    rec["excertos"] = exs
    vs.append(rec)
A["verbatins_citados"] = {"n_fontes": len(vs), "n_excertos": sum(len(r["excertos"]) for r in vs),
                          "fontes_sha_ok": sum(1 for r in vs if r["sha_ok"]),
                          "fontes_sha_diverge": [(r["id"], r["sha_registrado"], r["sha_agora"], r["bytes_registrado"], r["bytes_agora"], r.get("prefixo_congelado_confere")) for r in vs if not r["sha_ok"]],
                          "excertos_ok": sum(1 for r in vs for e in r["excertos"] if e["ok"]),
                          "excertos_linha_ok": sum(1 for r in vs for e in r["excertos"] if e["linha_ok"]),
                          "excertos_falha": [(r["id"], e["id"]) for r in vs for e in r["excertos"] if not e["ok"]],
                          "lista": vs}
out["A_preregistro"] = A

# ---------- Parte B ----------
pb = rb(PEDRA)
B = {"pedra_sha_ok": sha(pb) == PEDRA_SHA, "pedra_bytes": len(pb)}
ptxt = pb.decode("utf-8")
cands = {}


def add(p):
    try:
        cands[p] = rb(p)
    except Exception as e:
        pass


add(t["arquivo"])
for v in pre["verbatins_citados"]:
    add(v["arquivo"])
add(os.path.join(BASE, "1_PREREGISTRO", "PREREGISTRO.md"))
add(PRE)
add(r"C:\Users\rotol\.claude\CLAUDE.md")
add(r"C:\IALD\CLAUDE.md")
for p in sorted(glob.glob(os.path.join(MEM, "*.md"))):
    add(p)
for dp, dn, fn in os.walk(LONG + KER):
    if "\\.lake" in dp:
        dn[:] = []
        continue
    for f in fn:
        if f.endswith(".lean"):
            add(os.path.join(dp, f)[len(LONG):])
# relatorios da rodada 1 (achados citados pelo nome) e resultados
for p in glob.glob(os.path.join(BASE, "4_RELATORIO", "*.md")) + glob.glob(os.path.join(BASE, "4_RELATORIO", "AUDITORIAS", "**", "*.md"), recursive=True):
    add(p)
B["n_fontes_candidatas"] = len(cands)
# texto JSON do pre-registro decodificado (as strings), para citacoes do pre-registro
pre_strings = []


def collect(x):
    if isinstance(x, str):
        pre_strings.append(x)
    elif isinstance(x, dict):
        for v in x.values():
            collect(v)
    elif isinstance(x, list):
        for v in x:
            collect(v)


collect(pre)
pre_join = "\n".join(pre_strings)


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


norm_cache = {p: norm(b.decode("utf-8", "replace")) for p, b in cands.items()}
norm_cache["<PREREGISTRO.json strings>"] = norm(pre_join)
quotes = []
for m in re.finditer(r"«(.*?)»", ptxt, flags=re.S):
    q = m.group(1)
    line = ptxt[:m.start()].count("\n") + 1
    qb = q.encode("utf-8")
    exact = [p for p, b in cands.items() if qb in b]
    if q in pre_join:
        exact.append("<PREREGISTRO.json strings>")
    nq = norm(q)
    normed = [p for p, s in norm_cache.items() if nq in s] if not exact else []
    ctx_start = ptxt.rfind("\n", 0, m.start()) + 1
    ctx = ptxt[ctx_start:ptxt.find("\n", m.end())]
    quotes.append({"linha": line, "citacao": q, "multilinha": "\n" in q, "exato_em": [os.path.basename(p) for p in exact],
                   "exato_no_operador_12out": qb in ob, "normalizado_em": [os.path.basename(p) for p in normed],
                   "contexto": ctx[:300]})
B["n_citacoes"] = len(quotes)
B["exatas"] = sum(1 for q in quotes if q["exato_em"])
B["so_normalizadas"] = [(q["linha"], q["citacao"][:80], q["normalizado_em"][:4]) for q in quotes if not q["exato_em"] and q["normalizado_em"]]
B["nao_achadas"] = [(q["linha"], q["citacao"][:120]) for q in quotes if not q["exato_em"] and not q["normalizado_em"]]
B["lista"] = quotes
out["B_pedra"] = B
with open(sys.argv[1], "w", encoding="utf-8") as fo:
    json.dump(out, fo, indent=1, ensure_ascii=False)
print("A: arquivo", A["arquivo_sha_ok"], A["arquivo_bytes_ok"], "crlf", A["crlf"], "| segunda parte", A["segunda_parte"]["sha_ok"], A["segunda_parte"]["vai_ate_o_fim"], A["segunda_parte"]["comeca_certo"],
      "| frases", A["frases"]["n"], A["frases"]["todas_ok"], "fora:", A["frases"]["bytes_da_segunda_parte_fora_das_frases"], A["frases"]["fora_so_espaco_e_marcacao"])
vc = A["verbatins_citados"]
print("A: fontes", vc["n_fontes"], "sha_ok", vc["fontes_sha_ok"], "diverge", vc["fontes_sha_diverge"], "| excertos", vc["n_excertos"], "ok", vc["excertos_ok"], "linha_ok", vc["excertos_linha_ok"], "falha", vc["excertos_falha"])
print("B: pedra sha ok", B["pedra_sha_ok"], "| citacoes", B["n_citacoes"], "exatas", B["exatas"], "| fontes candidatas", B["n_fontes_candidatas"])
print("B so normalizadas:")
for x in B["so_normalizadas"]:
    print("  ", x)
print("B nao achadas:")
for x in B["nao_achadas"]:
    print("  ", x)
