"""CU-F1: estrutura do HARNESS_TEXTOS_ENSAIO_v411.json e do rascunho do X; contagem de strings; README projetado (tamanho do arquivo medido)."""
import hashlib, json, os, re
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
sha16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
hp = os.path.join(V, "pos_rito", "HARNESS_TEXTOS_ENSAIO_v411.json")
rp = os.path.join(V, "pos_rito", "CUSTODIA_v411_RASCUNHO.txt")
print("harness sha16", sha16(hp), os.path.getsize(hp), "| rascunho sha16", sha16(rp), os.path.getsize(rp))
H = json.load(open(hp, encoding="utf-8"))
print("chaves:", list(H.keys()))


def walk(x, p, out, depth=0):
    if isinstance(x, str):
        out.append((p, x))
    elif isinstance(x, dict):
        for k, v in x.items():
            walk(v, p + "/" + str(k), out, depth + 1)
    elif isinstance(x, list):
        for i, v in enumerate(x):
            walk(v, p + "[%d]" % i, out, depth + 1)


out = []
walk(H, "", out)
print("strings:", len(out), "| >200 chars:", sum(1 for _, s in out if len(s) > 200), "| >2000:", sum(1 for _, s in out if len(s) > 2000))
# o maior grupo de caminhos
from collections import Counter
c = Counter(re.sub(r"\[\d+\]", "[]", p).split("/")[1] if "/" in p else p for p, _ in out)
print("strings por chave de topo:", dict(c))
for k in H:
    v = H[k]
    print("  ", k, type(v).__name__, (list(v.keys())[:8] if isinstance(v, dict) else (len(v) if isinstance(v, list) else str(v)[:60])))
# README projetado
rd = r"C:\t\k411c\ensaio_topo_proposto\pos_rito_blocos\README_PROJETADO_v411.md"
if os.path.exists(rd):
    import datetime
    print("README_PROJETADO_v411.md bytes:", os.path.getsize(rd), "| mtime", datetime.datetime.fromtimestamp(os.path.getmtime(rd)).strftime("%d/%m %H:%M:%S"), "| sha16", sha16(rd))
hd = r"C:\t\k411c\ensaio_topo_proposto\pos_rito_blocos\HANDOFF_v411_CUSTODIA.md"
if os.path.exists(hd):
    import datetime
    print("HANDOFF de ensaio bytes:", os.path.getsize(hd), "| mtime", datetime.datetime.fromtimestamp(os.path.getmtime(hd)).strftime("%d/%m %H:%M:%S"))
P = json.load(open(os.path.join(V, "PRONTO_POS_RITO_v411.json"), encoding="utf-8"))
print("PRONTO_POS_RITO quando:", P.get("quando"), "| readme_projetado_bytes:", P["readme"]["readme_projetado_bytes"], "| hoje:", P["readme"]["readme_hoje_bytes"], "| teto:", P["readme"]["teto_bytes"])
print("README real hoje (se existir a copia espelho):")
for cand in (r"C:\IALD\Artigo\the_boundary\README.md", r"C:\IALD\Central de Patentes\README.md"):
    if os.path.exists(cand):
        print("  ", cand, os.path.getsize(cand))
