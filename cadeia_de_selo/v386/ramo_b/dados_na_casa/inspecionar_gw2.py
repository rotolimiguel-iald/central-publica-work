import json, hashlib, os
def sha16(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]
def keys_of(o, depth=0, maxd=1, prefix=""):
    out = []
    if isinstance(o, dict):
        for k, v in list(o.items())[:50]:
            t = type(v).__name__
            extra = f" (n={len(v)})" if isinstance(v, (list, dict)) else ""
            out.append(f"{prefix}{k}: {t}{extra}")
            if depth < maxd and isinstance(v, dict):
                out += keys_of(v, depth + 1, maxd, prefix + "  ")
            elif depth < maxd and isinstance(v, list) and v and isinstance(v[0], dict):
                out.append(f"{prefix}  [0] keys: {list(v[0].keys())[:40]}")
    elif isinstance(o, list):
        out.append(f"{prefix}list n={len(o)}; [0]={str(o[0])[:300] if o else ''}")
    return out
base = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache"
def load(rel):
    p = os.path.join(base, rel)
    print("=" * 90); print(rel, f"bytes={os.path.getsize(p)} sha16={sha16(p)}")
    with open(p, "rb") as f: return json.loads(f.read().decode("utf-8"))
for rel in [r"gw\GWOSC_WINDOWS_V1.manifest.json", r"gw\GWOSC_ECHO_WINDOWS_V1.manifest.json", r"gw\GWOSC_O4_32S_V1.manifest.json",
            r"bancada_01out\remanescentes_v3.json", r"bancada_01out\AMOSTRA_FASE6.json",
            r"bancada_01out\PREREGISTRO_FASE6_ECO_RADICAL_20261001.json", r"CHAIN_OF_CUSTODY.json"]:
    o = load(rel)
    for l in keys_of(o)[:60]: print("  " + l)
    if isinstance(o, dict):
        for k in ("path", "source_dir", "dir", "root", "npz", "cache_dir", "catalog", "events", "series", "n_events", "n_series", "origem", "fonte", "versao", "version", "windows", "out", "arquivo"):
            if k in o:
                v = o[k]
                print(f"  >> {k} = {str(v)[:500]}")
# ringdown V2 details
o = load(r"gw\RINGDOWN_DEPHASING_V2_RESULT.json")
for k in ("version","amendment_of","executed","instrument","beta","t_planck","prediction","pipeline","catalog","n_events","n_no_template","n_on_edge","stacks","start_systematic"):
    print(f"  >> {k} = {json.dumps(o.get(k), ensure_ascii=False)[:1200]}")
ps = o["per_series"]
print("  >> per_series n =", len(ps)); print("  >> per_series[0] =", json.dumps(ps[0], ensure_ascii=False)[:1500])
statuses = {}
for s in ps: statuses[s.get("status")] = statuses.get(s.get("status"), 0) + 1
print("  >> status counts:", statuses)
evs = sorted({s["event"] for s in ps}); print("  >> n distinct events:", len(evs)); print("  >> events:", evs)
# ringdown V1
o = load(r"gw\RINGDOWN_DEPHASING_V1_RESULT.json")
for k in ("version","executed","instrument","prediction","pipeline","catalog","n_events","stacks","start_systematic"):
    print(f"  >> {k} = {json.dumps(o.get(k), ensure_ascii=False)[:900]}")
# C6
o = load(r"gw\C6_RESULTS_GW250114.json")
for k in ("status","reason","registration_sha256","on_source_strain_read","scope","do_not_combine","code_sha256","convergence"):
    print(f"  >> {k} = {json.dumps(o.get(k), ensure_ascii=False)[:1500]}")
print("  >> files:"); 
for f in o["files"]: print("     ", json.dumps(f, ensure_ascii=False)[:300])
print("  >> results[0] =", json.dumps(o["results"][0], ensure_ascii=False)[:1200])
rs = o["results"]; print("  >> readings:", sorted({r.get("reading") for r in rs}), "starts:", sorted({r.get("start_tM") for r in rs}))
# H2
o = load(r"gw\H2_REPRODUCTION_V1_RESULT.json")
for k in ("version","executed","instrument","scripts","catalog","pipeline"):
    print(f"  >> {k} = {json.dumps(o.get(k), ensure_ascii=False)[:800]}")
# ECHO V3
o = load(r"gw\ECHO_ANCHORED_V3_RESULT.json")
for k in ("fase","preregistro_sha256","instrumento","n_series_cego","n_series_abrir","faltam","veredito_principal"):
    print(f"  >> {k} = {json.dumps(o.get(k), ensure_ascii=False)[:900]}")
r = o["resultados"]["todos"]["KMS"]; print("  >> resultados.todos.KMS keys:", list(r.keys()))
