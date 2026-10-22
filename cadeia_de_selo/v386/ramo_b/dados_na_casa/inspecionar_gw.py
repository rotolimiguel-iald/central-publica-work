import json, hashlib, os, sys
io_out = []
def sha16(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]
def keys_of(o, depth=0, maxd=2, prefix=""):
    out = []
    if isinstance(o, dict):
        for k, v in list(o.items())[:60]:
            t = type(v).__name__
            extra = ""
            if isinstance(v, (list, dict)):
                extra = f" (n={len(v)})"
            out.append(f"{prefix}{k}: {t}{extra}")
            if depth < maxd and isinstance(v, dict):
                out += keys_of(v, depth + 1, maxd, prefix + "  ")
            elif depth < maxd and isinstance(v, list) and v and isinstance(v[0], dict):
                out.append(f"{prefix}  [0] keys: {list(v[0].keys())[:40]}")
    return out
base = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache"
files = [
 r"gw\C6_RESULTS_GW250114.json",
 r"gw\RINGDOWN_DEPHASING_V1_RESULT.json",
 r"gw\RINGDOWN_DEPHASING_V2_RESULT.json",
 r"gw\H2_REPRODUCTION_V1_RESULT.json",
 r"gw\ECHO_ANCHORED_V3_RESULT.json",
 r"gw\ECHO_PE_V2_RESULT.json",
 r"gw\ECHO_SEARCH_V1_RESULT.json",
 r"gw\GWOSC_WINDOWS_V1.manifest.json",
 r"gw\GWOSC_ECHO_WINDOWS_V1.manifest.json",
 r"gw\GWOSC_O4_32S_V1.manifest.json",
 r"bancada_01out\remanescentes_v3.json",
 r"bancada_01out\AMOSTRA_FASE6.json",
 r"bancada_01out\PREREGISTRO_FASE6_ECO_RADICAL_20261001.json",
 r"bancada_01out\RESULTADO_V5_FASE6_20261001.json",
 r"bancada_01out\PODER_V5_ANTES_DE_ABRIR.json",
 r"CHAIN_OF_CUSTODY.json",
]
for rel in files:
    p = os.path.join(base, rel)
    print("=" * 100)
    print(rel)
    if not os.path.exists(p):
        print("  AUSENTE"); continue
    print(f"  bytes={os.path.getsize(p)} sha16={sha16(p)}")
    try:
        with open(p, "rb") as f:
            raw = f.read()
        o = json.loads(raw.decode("utf-8"))
    except Exception as e:
        print("  JSON ERRO:", e); continue
    for line in keys_of(o)[:120]:
        print("  " + line)
