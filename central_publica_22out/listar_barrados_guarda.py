# -*- coding: utf-8 -*-
"""Lista (SÓ LEITURA, saída local) os arquivos do núcleo que a guarda de marcadores privados barrou, separando: (a) marcadores PRIVADOS
(~/.iald_privado) e (b) só os termos da casa (GUARDA); e, para (b), se o MESMO conteúdo já está publicado no the_boundary (sha256 no
espelho atual ou nos backups de versão)."""
import hashlib, json, re, subprocess, sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"C:\IALD\Site\tgl\v3.0_bancada\tools")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import custodia_v395_espelho as GU  # noqa: E402
from mascara_pii import mascarar     # noqa: E402

SRC = Path(r"C:\IALD\Central de Patentes")
DST = Path(r"C:\IALD\Central_publica\central-publica")
tr = subprocess.run(["git", "-C", str(SRC), "ls-files", "-z"], capture_output=True).stdout.decode("utf-8", "replace").split("\0")
idx = {a["caminho"] for a in json.loads((DST / "INDICE_PUBLICO.json").read_text(encoding="utf-8"))["arquivos"]}
pub = set()
for base in (Path(r"C:\IALD\Artigo\the_boundary"), Path(r"C:\IALD\Artigo\the_boundary_BACKUPS")):
    for p in base.rglob("*"):
        if p.is_file() and p.suffix.lower() in (".py", ".md", ".json", ".txt", ".tex") and p.stat().st_size < 60 * 1024 * 1024 and ".git" not in p.parts:
            pub.add(hashlib.sha256(p.read_bytes()).hexdigest())
priv, casa, casa_pub = Counter(), Counter(), Counter()
lista = []
for t in tr:
    if not t or t in idx:
        continue
    p = SRC / t
    if not p.is_file() or p.suffix.lower() not in (".py", ".md", ".json", ".txt", ".tex", ".csv", ".yaml", ".yml", ".html", ".jsonl", ".lean"):
        continue
    if p.stat().st_size > 25 * 1024 * 1024:
        continue
    txt = p.read_bytes().decode("utf-8", "replace")
    n_priv = sum(len(g.findall(txt)) for g in GU.PRIV)
    n_casa = sum(len(g.findall(txt)) for g in GU.GUARDA)
    if not (n_priv or n_casa):
        continue
    top = "/".join(t.split("/")[:2]) if t.startswith(("vault/", "patents/")) else t.split("/")[0]
    if n_priv:
        priv[top] += 1
    else:
        casa[top] += 1
        if hashlib.sha256(p.read_bytes()).hexdigest() in pub:
            casa_pub[top] += 1
    lista.append({"caminho": t, "privados": n_priv, "casa": n_casa})
Path(r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\f50b1d05-8292-4283-87ca-6534734053b5\scratchpad\barrados_guarda.json").write_text(
    json.dumps(lista, ensure_ascii=False), encoding="utf-8")
print("com marcador PRIVADO:", sum(priv.values()), priv.most_common(12))
print("só termos da casa:", sum(casa.values()), casa.most_common(12))
print("   destes, já publicados byte a byte no the_boundary:", sum(casa_pub.values()), casa_pub.most_common(12))
