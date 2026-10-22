"""json_walk.py <arquivo> [regex de campos] [profundidade]: imprime sha256 e os campos cujo caminho casa com o regex (so leitura)."""
import json, hashlib, re, sys
f = sys.argv[1]; rx = re.compile(sys.argv[2] if len(sys.argv) > 2 else r"verdict|veredito|z_|sigma|lnB|ln_B|bayes|power|poder|tens|beta|H0|resumo|summary|conclus|status|custo|cost|cpu|disc", re.I)
maxd = int(sys.argv[3]) if len(sys.argv) > 3 else 4
raw = open(f, "rb").read(); print(f"### {f}\n    sha256 {hashlib.sha256(raw).hexdigest()}  {len(raw)} B")
d = json.loads(raw.decode("utf-8")); print("    top keys:", list(d.keys())[:40] if isinstance(d, dict) else type(d))
out = []
def walk(o, path="", depth=0):
    if depth > maxd: return
    if isinstance(o, dict):
        for k, v in o.items():
            p = f"{path}.{k}" if path else k
            if isinstance(v, (dict, list)): walk(v, p, depth+1)
            elif rx.search(p): out.append(f"  {p} = {json.dumps(v, ensure_ascii=False)[:300]}")
    elif isinstance(o, list) and o and isinstance(o[0], dict) and len(o) <= 15:
        for i, it in enumerate(o): walk(it, f"{path}[{i}]", depth+1)
walk(d); print("\n".join(out[:120]))
