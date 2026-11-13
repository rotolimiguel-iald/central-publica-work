"""CU-G1: confere a tabela do pedido (secao 1) contra o disco: sha16 e bytes lidos agora."""
import hashlib, os, re
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
txt = open(os.path.join(V, "revisao_terceiro", "PEDIDO_CONFERENCIA_UNICA_v411.md"), "rb").read().decode("utf-8")
rows = re.findall(r"^\| (.+?) \| `([^`]+)` \| `([0-9a-f]{16})` \| (\d+) \|$", txt, re.M)
print("linhas da tabela:", len(rows))
bad = 0
for desc, path, h, nb in rows:
    p = path if re.match(r"^[A-Za-z]:\\", path) else os.path.join(V, path.replace("/", os.sep))
    if not os.path.exists(p):
        print("AUSENTE:", path)
        bad += 1
        continue
    b = open(p, "rb").read()
    h2 = hashlib.sha256(b).hexdigest()[:16]
    ok = (h2 == h and len(b) == int(nb))
    if not ok:
        bad += 1
        print("DIFERE:", path, "| tabela", h, nb, "| disco", h2, len(b))
print("divergencias:", bad)
