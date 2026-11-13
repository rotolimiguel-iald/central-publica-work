# Quais links públicos apontam para um caminho que viraria referência (a cópia sai da árvore do GitHub)? Só leitura.
# Reproduz a escolha do original da primeira aplicação (todas as cópias já publicadas): fixos primeiro, depois o menor caminho.
import json, os, re, sys, urllib.parse
from collections import defaultdict
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"C:\IALD\Central de Patentes\work\central_publica_22out")
import copias_referencia as CR
PUB = Path(r"C:\IALD\Central_publica")
refs = {}
for r in ("central-publica", "central-publica-work", "central-publica-bancada"):
    g = defaultdict(list)
    for a in json.loads((PUB / r / "INDICE_PUBLICO.json").read_text(encoding="utf-8"))["arquivos"]:
        g[(a["sha256"], a["bytes"])].append(a["caminho"])
    s = set()
    for m in g.values():
        if len(m) < 2: continue
        orig = sorted(m, key=lambda x: (0 if CR.fixo(x) else 1, x))[0]
        s |= {x for x in m if x != orig and not CR.fixo(x)}
    refs[r] = s
    print(r, "referências:", len(s))
URL = re.compile(r"https?://(?:raw\.githubusercontent\.com/rotolimiguel-iald/(central-publica(?:-work|-bancada)?)/(?:refs/heads/)?main/|github\.com/rotolimiguel-iald/(central-publica(?:-work|-bancada)?)/(?:blob|raw)/main/)([^\s\)\]\"'<>`|#?]+)")
FONTES = [Path(r"C:\IALD\Artigo\the_boundary"), Path(r"C:\IALD\Site\tgl\v3.0")] + [PUB / r for r in refs]
EXT = {".md", ".json", ".txt", ".html", ".xml", ".js", ".cff", ".tex", ".py"}
achados, links, arqs = defaultdict(set), 0, 0
for base in FONTES:
    for dp, dns, fns in os.walk(base):
        dns[:] = [x for x in dns if x not in (".git", "node_modules")]
        if base in [PUB / r for r in refs] and os.path.relpath(dp, base) not in (".",):   # nos preparos, só a raiz (README, llms.txt)
            dns[:] = []
        for f in fns:
            if os.path.splitext(f)[1].lower() not in EXT: continue
            p = os.path.join(dp, f)
            try:
                t = open(p, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            arqs += 1
            for m in URL.finditer(t):
                links += 1
                repo = m.group(1) or m.group(2)
                cam = urllib.parse.unquote(m.group(3))
                if cam in refs[repo]:
                    achados[(repo, cam)].add(os.path.relpath(p, base.parent))
print("arquivos lidos: %d | links para os três repositórios: %d | links para caminho que viraria referência: %d" % (arqs, links, len(achados)))
for (repo, cam), onde in sorted(achados.items())[:40]:
    print("  %s/%s  <-  %s" % (repo, cam, sorted(onde)[:3]))
# links de PASTA (/tree/main/<pasta>): a pasta some do GitHub se todos os arquivos dela virarem referência
TREE = re.compile(r"https?://github\.com/rotolimiguel-iald/(central-publica(?:-work|-bancada)?)/tree/main/([^\s\)\]\"'<>`|#?]+)")
pastas = defaultdict(set)
for base in FONTES:
    for dp, dns, fns in os.walk(base):
        dns[:] = [x for x in dns if x not in (".git", "node_modules")]
        if base in [PUB / r for r in refs] and os.path.relpath(dp, base) != ".":
            dns[:] = []
        for f in fns:
            if os.path.splitext(f)[1].lower() not in EXT: continue
            try:
                t = open(os.path.join(dp, f), encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            for m in TREE.finditer(t):
                pastas[(m.group(1), urllib.parse.unquote(m.group(2)).rstrip("/"))].add(f)
vazias = []
for (repo, pasta), onde in sorted(pastas.items()):
    idxp = [a["caminho"] for a in json.loads((PUB / repo / "INDICE_PUBLICO.json").read_text(encoding="utf-8"))["arquivos"] if a["caminho"].startswith(pasta + "/")]
    fica = [x for x in idxp if x not in refs[repo]]
    if idxp and not fica:
        vazias.append((repo, pasta, len(idxp)))
print("links de pasta: %d | pastas que ficariam vazias no GitHub: %d %s" % (len(pastas), len(vazias), vazias[:10]))
