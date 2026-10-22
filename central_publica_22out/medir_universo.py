# -*- coding: utf-8 -*-
"""Mede (SÓ LEITURA) o universo da liberação pública da Central (22/10/2026): tamanho e contagem por região, arquivos acima do limite do
GitHub (100 MB), e candidatos a dado pessoal por tipo (e-mails, mensagens assinadas, planilhas e formulários)."""
import json, os, subprocess, sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
C = Path(r"C:\IALD\Central de Patentes")
EXCL_DIR = {".git", ".venv", "venv", "node_modules", "__pycache__", ".lake", "tex_environment", ".wheels_ipv4", "unsloth_compiled_cache"}
EMAIL = {".eml", ".msg", ".p7m", ".mbox", ".pst", ".ost"}
GH_LIM = 100 * 1024 * 1024


def walk(base):
    n = b = 0; big = []; ext = Counter(); mail = 0; bak = 0
    for dp, dns, fns in os.walk(base):
        dns[:] = [d for d in dns if d not in EXCL_DIR]
        for f in fns:
            p = os.path.join(dp, f)
            try:
                s = os.path.getsize(p)
            except OSError:
                continue
            if ".bak_" in f or f.endswith((".tmp",)):
                bak += 1; continue
            e = os.path.splitext(f)[1].lower()
            if e in EMAIL:
                mail += 1
            n += 1; b += s; ext[e] += s
            if s > GH_LIM:
                big.append((s, os.path.relpath(p, C)))
    return n, b, big, ext, mail, bak


tr = subprocess.run(["git", "-C", str(C), "ls-files", "-z"], capture_output=True).stdout.decode("utf-8", "replace").split("\0")
tr = [t for t in tr if t]
tb = sum(os.path.getsize(C / t) for t in tr if (C / t).is_file())
print("RASTREADO (git): %d arquivos, %.2f GB" % (len(tr), tb / 2**30))
for reg in ("work", "EPCT", "backend", "frontend", "Patentes", "memory", "vault"):
    n, b, big, ext, mail, bak = walk(C / reg)
    print("%-10s %7d arquivos  %7.2f GB | >100MB: %d | e-mails/mensagens: %d | backups pulados: %d | maiores tipos: %s" % (
        reg, n, b / 2**30, len(big), mail, bak, ", ".join("%s %.1fG" % (k or "(sem)", v / 2**30) for k, v in ext.most_common(4))))
    for s, r in sorted(big, reverse=True)[:4]:
        print("     > %.0f MB %s" % (s / 2**20, r[:150]))
snaps = sorted(d for d in (C.parent / "Central de Patentes_BACKUPS").iterdir() if d.name.startswith("Chatgpt_") and (d / "MANIFEST.json").is_file())
m = json.loads((snaps[-1] / "MANIFEST.json").read_text(encoding="utf-8"))
arq = m["arquivos"]
cb = sum(v.get("bytes", 0) for v in arq.values())
cbig = [(v.get("bytes", 0), k) for k, v in arq.items() if v.get("bytes", 0) > GH_LIM]
cmail = sum(1 for k in arq if os.path.splitext(k)[1].lower() in EMAIL)
print("CHATGPT/ (manifesto %s): %d arquivos, %.2f GB (sem .lake, tex_environment e >25 MB, que somam %d + %d + %d arquivos) | e-mails: %d" % (
    snaps[-1].name, len(arq), cb / 2**30, m["excluidos"]["lake"]["n"], m["excluidos"]["tex_environment"]["n"], m["excluidos"]["maiores_que_25MB"]["n"], cmail))
print("   >25 MB fora do snapshot: %.1f GB" % (m["excluidos"]["maiores_que_25MB"]["bytes"] / 2**30))
