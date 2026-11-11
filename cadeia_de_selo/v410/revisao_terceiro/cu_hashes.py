import glob, hashlib, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
from cu_corpus import *
WK = "C:/IALD/Central de Patentes/work/"
def segs(t): return [s.strip() for s in re.split(r"(?<=[.;:])\s+", ws(t)) if s.strip()]
tok16 = re.compile(r"(?<![0-9a-fA-F])([0-9a-f]{16})(?![0-9a-fA-F])"); tok64 = re.compile(r"(?<![0-9a-fA-F])([0-9a-f]{64})(?![0-9a-fA-F])")
alvos = {}
C = carregar()
for k in ("pt", "en", "md"):
    velho = set(segs(rd("cu_saidas/novo_%s.R3.txt" % k)))
    alvos[k] = " ".join(s for s in segs(rd("novo_%s.txt" % k)) if s not in velho)
alvos["custodia"] = C["custodia_ws"]; alvos["readme"] = open("cu_saidas/readme_render.json", encoding="utf-8").read()
alvos["registros_v410"] = " ".join(t for p, t in todos_registros(C))
toks = {}
for k, t in alvos.items():
    for m in tok16.finditer(t): toks.setdefault(m.group(1), set()).add(k)
    for m in tok64.finditer(t): toks.setdefault(m.group(1)[:16], set()).add(k + ":64")
print("tokens sha16 distintos nos alvos:", len(toks))
t0 = time.time()
# conjunto de hashes calculados
dirs = [R + "*", R + "insumos/*", R + "pedra/*", R + "pos_rito/*", R + "conserto_r3/*", R + "kernel/*", R + "orquestrador/*", WK + "cunhagens_13out/*", R + "insumos/cunhagens/*", R + "dry_v410/*", R + "base_v409/*", R + "dry_v410/tgl_kernel/TGLExt/AEscala.lean"]
S = {}
for pat in dirs:
    for p in glob.glob(pat):
        if os.path.isfile(p) and os.path.getsize(p) < 80_000_000 and "revisao_terceiro" not in p:
            try: h = hashlib.sha256(open(p, "rb").read()).hexdigest()
            except Exception: continue
            S[h[:16]] = p
print("arquivos hasheados:", len(S), "| %.0f s" % (time.time() - t0))
# texto de recibos (hashes declarados em JSON/MD/py do pacote)
txtr = ""
for pat in (R + "*.json", R + "*.md", R + "insumos/*.json", R + "pos_rito/*.json", R + "kernel/*.json", R + "conserto_r3/*.json", R + "conserto_r3/*.md", WK + "cunhagens_13out/*.json"):
    for p in glob.glob(pat):
        if os.path.getsize(p) < 30_000_000: txtr += open(p, "rb").read().decode("utf-8", "replace")
for pat in (R + "delta_v410.py", R + "registros_*.py", R + "pos_rito/*.py"):
    for p in glob.glob(pat): txtr += open(p, "rb").read().decode("utf-8", "replace")
res = {"calculado": [], "declarado_em_recibo": [], "NAO_ACHADO": []}
for tkn, ks in sorted(toks.items()):
    if tkn in S: res["calculado"].append(tkn)
    elif tkn in txtr: res["declarado_em_recibo"].append(tkn)
    else: res["NAO_ACHADO"].append((tkn, sorted(ks)))
print({k: len(v) for k, v in res.items()})
for t, ks in res["NAO_ACHADO"]: print("   NAO ACHADO:", t, ks)
json.dump(res, open("cu_saidas/cu_hashes_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
