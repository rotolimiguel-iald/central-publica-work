"""A2 — Auditor F1.TEMPO (lente REPRODUCAO): verbatins, byte a byte, so leitura.
(a) texto do operador 12/10: sha256, bytes, CRLF; inicio da segunda parte achado POR BUSCA (nao pelo offset
    declarado) e comparado com o declarado; sha256 da segunda parte;
(b) as 23 frases: bytes no offset == texto UTF-8, sha256; segmentacao INDEPENDENTE do auditor
    (regra declarada: '. ' seguido de maiuscula, por paragrafo) comparada com a lista;
(c) verbatins_citados (14 fontes, 30 excertos): sha256 do arquivo agora x declarado; cada excerto no offset,
    sha256 e linha;
(d) mapeamento_excertos: cada sha256 bate com o do excerto;
(e) aspas «…» da PEDRA: cada uma procurada (normalizada so para marcacao markdown e aspas tipograficas) no texto
    de 12/10, nas fontes citadas e no kernel do Nos; o que nao aparece e listado para leitura humana;
(f) aspas «…» do PREREGISTRO.json atribuidas ao operador: mesma busca.
Saida: JSON no caminho dado."""
import glob
import hashlib
import json
import os
import re
import sys
import unicodedata

PRE = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\1_PREREGISTRO\PREREGISTRO.json"
STONE = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\3_KERNEL\sandbox\TheTimeHasNoRank.lean"
OPTXT = r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt"
KROOT = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt"
MEMDIR = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"

out = {"falhas": 0, "checks": []}


def chk(item, esperado, lido, extra=None):
    ok = esperado == lido
    rec = {"item": item, "ok": ok}
    if not ok:
        rec.update({"esperado": esperado, "lido": lido})
        out["falhas"] += 1
    if extra:
        rec.update(extra)
    out["checks"].append(rec)
    return ok


def sha(b):
    return hashlib.sha256(b).hexdigest()


d = json.load(open(PRE, encoding="utf-8"))
raw = open(OPTXT, "rb").read()
t = d["texto_do_operador"]
chk("12/10 sha256", t["sha256"], sha(raw))
chk("12/10 bytes", t["bytes"], len(raw))
chk("12/10 crlf", t["crlf"], raw.count(b"\r\n"))
inicio = "O que mais me fascina é a impossibilidade de definição do tempo.".encode("utf-8")
off = raw.find(inicio)
chk("12/10 inicio da 2a parte achado por busca == offset declarado", t["segunda_parte"]["byte_offset"], off)
chk("12/10 inicio unico", 1, raw.count(inicio))
seg = raw[off:]
chk("12/10 2a parte bytes (ate o fim)", t["segunda_parte"]["bytes"], len(seg))
chk("12/10 2a parte sha256", t["segunda_parte"]["sha256"], sha(seg))
linha_ini = raw[:off].count(b"\n") + 1
linha_fim = raw.rstrip(b"\n").count(b"\n") + 1
chk("12/10 2a parte linhas", t["segunda_parte"]["linhas"], f"{linha_ini}–{linha_fim}")

# (b) frases
frases = t["frases"]
chk("n_frases", 23, len(frases))
for f in frases:
    o, n = f["byte_offset"], f["bytes"]
    b = raw[o:o + n]
    chk(f"frase {f['id']} bytes no offset", f["texto"].encode("utf-8"), b)
    chk(f"frase {f['id']} sha256", f["sha256"], sha(b))
    chk(f"frase {f['id']} linha", f["linha"], raw[:o].count(b"\n") + 1)
# segmentacao independente
txt2 = seg.decode("utf-8")
paras = [p for p in txt2.split("\n") if p.strip()]
mine = []
for p in paras:
    parts = re.split(r"(?<=\.) (?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ])", p)
    mine.extend(parts)
chk("segmentacao do auditor: n", len(frases), len(mine))
chk("segmentacao do auditor == lista do pre-registro", [f["texto"] for f in frases], mine)
# cobertura: as frases reconstroem os paragrafos
rec_ok = all(any(fr["texto"] in p for p in paras) for fr in frases)
chk("toda frase esta num paragrafo", True, rec_ok)

# (c) verbatins citados
src_texts = {"OPERADOR_12out": raw.decode("utf-8")}
exc_sha = {}
for v in d["verbatins_citados"]:
    p = v["arquivo"]
    try:
        b = open(p, "rb").read()
    except OSError as e:
        chk(f"fonte {v['id']} legivel", True, False, {"erro": str(e)})
        continue
    src_texts[v["id"]] = b.decode("utf-8", errors="replace")
    sha_ok = chk(f"fonte {v['id']} sha256 (agora x declarado)", v["sha256"], sha(b),
                 {"arquivo": p, "bytes_agora": len(b)})
    chk(f"fonte {v['id']} bytes", v["bytes"], len(b))
    chk(f"fonte {v['id']} sha16_confere declarado", True, v.get("sha16_confere"))
    for e in v["excertos"]:
        o, n = e["byte_offset"], e["bytes"]
        eb = e["texto"].encode("utf-8")
        chk(f"excerto {v['id']}/{e['id']} bytes no offset", eb, b[o:o + n],
            {"achado_em_outro_offset": b.find(eb)} if b[o:o + n] != eb else None)
        chk(f"excerto {v['id']}/{e['id']} sha256", e["sha256"], sha(eb))
        chk(f"excerto {v['id']}/{e['id']} len", n, len(eb))
        if "linha" in e:
            chk(f"excerto {v['id']}/{e['id']} linha", e["linha"], b[:o].count(b"\n") + 1)
        exc_sha[(v["id"], e["id"])] = e["sha256"]
n_exc = sum(len(v["excertos"]) for v in d["verbatins_citados"])
out["n_excertos"] = n_exc
# (d) mapeamento
chk("mapeamento_excertos: 30", 30, len(d["mapeamento_excertos"]))
for m in d["mapeamento_excertos"]:
    chk(f"mapeamento {m['fonte']}/{m['excerto']} sha256", exc_sha.get((m["fonte"], m["excerto"])), m["sha256"])
chk("mapeamento_frases: 23 e cada sha bate", True,
    len(d["mapeamento_frases"]) == 23 and all(
        mf["sha256"] == next(f["sha256"] for f in frases if f["id"] == mf["frase"]) and
        mf["texto"] == next(f["texto"] for f in frases if f["id"] == mf["frase"]) for mf in d["mapeamento_frases"]))


# (e)/(f) aspas
def norm(s):
    s = unicodedata.normalize("NFC", s)
    s = s.replace("**", "").replace("*", "")
    s = s.replace("“", '"').replace("”", '"').replace("’", "'")
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def norm_cf(s):
    return norm(s).casefold().rstrip(" .…")


corpus = {k: norm(v).casefold() for k, v in src_texts.items()}
# memoria (so .md do diretorio de memoria do projeto) e kernel TGLExt (.lean)
mem = {}
for p in glob.glob(os.path.join(MEMDIR, "*.md")):
    try:
        mem[os.path.basename(p)] = norm(open(p, encoding="utf-8", errors="replace").read()).casefold()
    except OSError:
        pass
ker = {}
for p in glob.glob(os.path.join(KROOT, "**", "*.lean"), recursive=True):
    try:
        ker[os.path.relpath(p, KROOT)] = norm(open(p, encoding="utf-8", errors="replace").read()).casefold()
    except OSError:
        pass
out["corpus"] = {"fontes_citadas": len(corpus), "memoria_md": len(mem), "kernel_lean": len(ker)}


def busca(q):
    qn = norm_cf(q)
    if not qn:
        return {}
    r = {"fontes": [k for k, v in corpus.items() if qn in v]}
    r["memoria"] = [k for k, v in mem.items() if qn in v][:5]
    r["kernel"] = [k for k, v in ker.items() if qn in v][:5]
    return r


QUOTE = re.compile(r"«([^«»]{1,400})»")
stone_txt = open(STONE, encoding="utf-8").read()
st = []
for m in QUOTE.finditer(stone_txt):
    q = m.group(1)
    linha = stone_txt[:m.start()].count("\n") + 1
    r = busca(q)
    achou = any(r.get(k) for k in ("fontes", "memoria", "kernel"))
    st.append({"linha": linha, "aspas": q, "achada": achou, "onde": r})
out["pedra_aspas"] = st
out["pedra_aspas_nao_achadas"] = [x for x in st if not x["achada"]]


def strings(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)
    elif isinstance(o, str):
        yield o


pq = {}
for s in strings(d):
    for m in QUOTE.finditer(s):
        pq.setdefault(m.group(1), 0)
        pq[m.group(1)] += 1
pre_res = []
for q, c in pq.items():
    r = busca(q)
    pre_res.append({"aspas": q, "ocorrencias": c, "achada": any(r.get(k) for k in ("fontes", "memoria", "kernel")),
                    "onde": r})
out["preregistro_aspas_total"] = len(pre_res)
out["preregistro_aspas_nao_achadas"] = [x for x in pre_res if not x["achada"]]

tmp = sys.argv[1] + ".tmp"
with open(tmp, "w", encoding="utf-8") as fo:
    json.dump(out, fo, indent=1, ensure_ascii=False)
os.replace(tmp, sys.argv[1])
print("falhas:", out["falhas"], "de", len(out["checks"]), "| excertos:", n_exc, "| corpus:", out["corpus"])
for c in out["checks"]:
    if not c["ok"]:
        print("FALHA:", json.dumps(c, ensure_ascii=False)[:600])
print("PEDRA aspas:", len(st), "nao achadas:", len(out["pedra_aspas_nao_achadas"]))
for x in out["pedra_aspas_nao_achadas"]:
    print("  l.%d «%s»" % (x["linha"], x["aspas"]))
print("PRE aspas distintas:", len(pre_res), "nao achadas:", len(out["preregistro_aspas_nao_achadas"]))
for x in out["preregistro_aspas_nao_achadas"]:
    print("  «%s» x%d" % (x["aspas"][:160], x["ocorrencias"]))
