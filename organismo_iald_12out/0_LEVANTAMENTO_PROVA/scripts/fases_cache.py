"""Le os RESULTADO_FASE* do cache do rito (A Ponte e o Um/cache) e a cronologia da novidade de uso: sha256 e campos de veredito."""
import json, hashlib, re, glob, os
files = sorted(glob.glob(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\bancada_30set\RESULTADO_FASE*.json") + glob.glob(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\bancada_01out\RESULTADO_FASE*.json"))
files.append(r"C:\IALD\Central de Patentes\work\scratch_6da8f00d\fase9_hubble\novidade_de_uso\CRONOLOGIA_NOVIDADE_DE_USO.json")
files.append(r"C:\IALD\Artigo\MCMC_V2_RAZAO\24_v12_por_lente.json")
kw = re.compile(r"verdict|veredito|z_|sigma|lnB|ln_B|bayes|power|poder|tension|tensao|beta|H0|resumo|summary|conclus|data|date|quando|cronolog|novidade|hash|sha", re.I)
def walk(o, path="", depth=0, out=None):
    if depth > 3: return
    if isinstance(o, dict):
        for k, v in o.items():
            p = f"{path}.{k}" if path else k
            if isinstance(v, (dict, list)): walk(v, p, depth+1, out)
            elif kw.search(k) or kw.search(p):
                s = json.dumps(v, ensure_ascii=False); out.append(f"  {p} = {s[:260]}")
    elif isinstance(o, list) and o and isinstance(o[0], dict) and len(o) <= 12:
        for i, it in enumerate(o): walk(it, f"{path}[{i}]", depth+1, out)
for f in files:
    if not os.path.exists(f): print("\n### AUSENTE:", f); continue
    raw = open(f, "rb").read(); print(f"\n### {f}\n    sha256 {hashlib.sha256(raw).hexdigest()}  {len(raw)} B")
    try: d = json.loads(raw.decode("utf-8"))
    except Exception as e: print("    (json?)", e); continue
    print("    top keys:", list(d.keys())[:40] if isinstance(d, dict) else type(d))
    out = []; walk(d, "", 0, out)
    for line in out[:90]: print(line)
