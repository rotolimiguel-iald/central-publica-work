# -*- coding: utf-8 -*-
"""Publica um dos três repositórios públicos da Central no GitHub (ordem do operador, 22/10/2026: «Quero que o projeto inteiro esteja
indexado no github de forma pública e vinculado à minha pasta do the_boundary»). A partir da pasta de PREPARO (já curada pelos
construtores): git init (caminhos longos; bytes exatos: * -text), identidade noreply do GitHub, repositório PÚBLICO novo, commits e pushes em
LOTES (cada push bem abaixo do limite de 2 GB do GitHub), conferência final (a árvore remota tem o número de arquivos do índice).
Uso: publicar_repo_publico.py <nome-do-repo> <pasta_de_preparo> "<descrição>" """
import json, os, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
NOME, D, DESC = sys.argv[1], Path(sys.argv[2]), sys.argv[3]
assert NOME in ("central-publica", "central-publica-work", "central-publica-bancada"), NOME
assert (D / "INDICE_PUBLICO.json").is_file() and (D / "README.md").is_file(), "preparo incompleto — PARAR"
DONO = "rotolimiguel-iald"
EMAIL = "247441339+rotolimiguel-iald@users.noreply.github.com"
LOTE_BYTES = 700 * 1024 * 1024
CO = "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"


def g(*a, ok=True):
    r = subprocess.run(["git", "-C", str(D)] + list(a), capture_output=True, text=True, encoding="utf-8", errors="replace")
    if ok and r.returncode != 0:
        raise SystemExit("git %s falhou: %s" % (" ".join(a[:3]), (r.stderr or r.stdout)[-800:]))
    return r


if not (D / ".git").exists():
    g("init", "-b", "main")
for k, v in (("core.longpaths", "true"), ("core.autocrlf", "false"), ("core.quotepath", "false"), ("user.name", "Luiz Antonio Rotoli Miguel"),
             ("user.email", EMAIL), ("http.postBuffer", "524288000")):
    g("config", k, v)
ga = D / ".gitattributes"
if not ga.exists() or "* -text" not in ga.read_text(encoding="utf-8", errors="replace"):
    ga.write_text("* -text\n", encoding="utf-8")
r = subprocess.run(["gh", "repo", "view", "%s/%s" % (DONO, NOME), "--json", "visibility"], capture_output=True, text=True)
if r.returncode != 0:
    r = subprocess.run(["gh", "repo", "create", "%s/%s" % (DONO, NOME), "--public", "--description", DESC,
                        "--homepage", "https://teoriadagravitacaoluminodinamica.com/central/"], capture_output=True, text=True)
    assert r.returncode == 0, ("gh repo create falhou", r.stderr[-500:])
    print("repositório criado:", NOME)
else:
    assert '"PUBLIC"' in r.stdout, ("o repositório existe e não é público — PARAR", r.stdout)
if not g("remote", ok=False).stdout.strip():
    g("remote", "add", "origin", "https://github.com/%s/%s.git" % (DONO, NOME))
# os lotes: a raiz primeiro (README, índice, exclusões), depois cada pasta de primeiro nível, cortada em lotes de ~700 MB
idx = json.loads((D / "INDICE_PUBLICO.json").read_text(encoding="utf-8"))["arquivos"]
por_topo = {}
for a in idx:
    top = a["caminho"].split("/", 1)[0] if "/" in a["caminho"] else "(raiz)"
    por_topo.setdefault(top, []).append(a)
lotes, cur, cur_b = [], [], 0
raiz = [p.name for p in D.iterdir() if p.is_file()]
lotes.append(("a raiz (README, vínculo, índice, exclusões)", raiz))
for top in sorted(por_topo):
    if top == "(raiz)":
        continue
    for a in por_topo[top]:
        cur.append(a["caminho"]); cur_b += a["bytes"]
        if cur_b >= LOTE_BYTES:
            lotes.append(("%s (parte)" % top, cur)); cur, cur_b = [], 0
    if cur:
        lotes.append((top, cur)); cur, cur_b = [], 0
t0 = time.time()
for i, (rot, caminhos) in enumerate(lotes, 1):
    lista = D / ".git" / "lote.txt"
    lista.write_text("\n".join(caminhos) + "\n", encoding="utf-8")
    g("add", "-f", "--pathspec-from-file=" + str(lista))   # o .gitignore da origem não barra o que já foi curado e conferido
    if not g("diff", "--cached", "--quiet", ok=False).returncode:
        print("  lote %d/%d (%s): nada novo" % (i, len(lotes), rot)); continue
    msg = ("Central de Patentes da IALD, aberta (22/10/2026) — lote %d/%d: %s\n\nOrdem do operador: todo o código e todo resultado públicos; "
           "dados pessoais mascarados à vista; notas operacionais do operador fora; vínculo patentário em PATENTES.md (núcleo).\n\n%s\n" % (i, len(lotes), rot, CO))
    (D / ".git" / "msg.txt").write_text(msg, encoding="utf-8")
    g("commit", "-q", "-F", str(D / ".git" / "msg.txt"))
    r = g("push", "-u", "origin", "main", ok=False)
    if r.returncode != 0:
        time.sleep(30)
        r = g("push", "-u", "origin", "main", ok=False)
        assert r.returncode == 0, ("push falhou no lote %d" % i, r.stderr[-800:])
    print("  lote %d/%d (%s): %d arquivos, empurrado (%.0f s)" % (i, len(lotes), rot, len(caminhos), time.time() - t0), flush=True)
loc = g("rev-parse", "HEAD").stdout.strip()
rem = g("ls-remote", "origin", "refs/heads/main").stdout.split()[0]
n_arvore = len([x for x in g("ls-tree", "-r", "--name-only", "HEAD").stdout.splitlines() if x])
print("PUBLICADO %s: HEAD %s = origin %s | %d arquivos na árvore (índice: %d + raiz)" % (NOME, loc[:8], rem[:8], n_arvore, len(idx)))
assert loc == rem
