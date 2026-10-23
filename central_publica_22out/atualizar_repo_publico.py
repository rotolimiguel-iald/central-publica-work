# -*- coding: utf-8 -*-
"""ATUALIZA um dos três repositórios públicos já publicados (22/10/2026, custódia v396: «Atualize tudo com a nova versão do um.py») a
partir do preparo já mesclado e CONFERIDO (conferir_preparos.py APROVADO — este script exige o relatório de conferência mais novo que o
índice). Põe no git EXATAMENTE o índice público: `git add -f` de todo caminho do índice (o .gitignore da origem, copiado como texto, não
barra o que foi curado), `git rm --cached` de todo caminho rastreado que saiu do índice, a raiz gerada (índice, exclusões, README,
.gitattributes); pathspec LITERAL (um nome com * ou [ não vira padrão). Um commit, push SEM força; no fim, a árvore remota tem o número de
arquivos do índice mais a raiz gerada. Uso: atualizar_repo_publico.py <nome-do-repo> <pasta_do_preparo> "<título do commit>" """
import json, os, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
W = Path(__file__).resolve().parent
NOME, D, TIT = sys.argv[1], Path(sys.argv[2]), sys.argv[3]
assert NOME in ("central-publica", "central-publica-work", "central-publica-bancada"), NOME
CO = "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
ENV = dict(os.environ, GIT_LITERAL_PATHSPECS="1")
RAIZ_GERADA = ["INDICE_PUBLICO.json", "EXCLUSOES_PUBLICAS.json", ".gitattributes",
               "llms.txt"]   # (23/10/2026) o mapa de máquina de cada repositório, curadoria à mão do Kimi: rastreado, fora do índice


def g(*a, ok=True):
    r = subprocess.run(["git", "-C", str(D)] + list(a), capture_output=True, text=True, encoding="utf-8", errors="replace", env=ENV)
    if ok and r.returncode != 0:
        raise SystemExit("git %s falhou: %s" % (" ".join(a[:3]), (r.stderr or r.stdout)[-800:]))
    return r


conf = W / ("varredura_conferencia_%s.json" % D.name)
cj = json.loads(conf.read_text(encoding="utf-8")) if conf.is_file() else {}
assert cj.get("aprovado") is True, ("a conferência completa não está aprovada — PARAR", cj)
idx_mt = (D / "INDICE_PUBLICO.json").stat().st_mtime
COBERTO = None                         # a completa mais nova que o índice cobre tudo
if conf.stat().st_mtime <= idx_mt:
    # senão, a conferência do DELTA (conferir_delta.py: o próprio conferidor, só no que difere do HEAD), mais nova que o índice e aprovada,
    # tem de cobrir cada arquivo que entra no commit (a raiz gerada — README, índice, exclusões — o conferidor não varre)
    dconf = W / ("varredura_conferencia_delta_%s.json" % D.name)
    assert dconf.is_file() and dconf.stat().st_mtime > idx_mt, "nem a conferência completa nem a do delta são mais novas que o índice — PARAR"
    dj = json.loads(dconf.read_text(encoding="utf-8"))
    assert dj.get("aprovado") is True, ("a conferência do delta não está aprovada — PARAR", dj.get("contagem"))
    COBERTO = set(dj.get("delta_conferido") or [])
assert g("rev-parse", "HEAD").stdout.strip() == g("rev-parse", "origin/main").stdout.strip(), "HEAD != origin/main antes — PARAR"
idx = [a["caminho"] for a in json.loads((D / "INDICE_PUBLICO.json").read_text(encoding="utf-8"))["arquivos"]]
raiz = [n for n in RAIZ_GERADA if (D / n).is_file()]
quer = set(idx) | set(raiz)
tem = set(x for x in g("ls-files", "-z").stdout.split("\0") if x)
sair = sorted(tem - quer)
lista = D / ".git" / "incr_add.txt"
lista.write_bytes(b"\0".join(x.encode("utf-8") for x in sorted(quer)))
g("add", "-f", "--pathspec-from-file=" + str(lista), "--pathspec-file-nul")
if sair:
    lr = D / ".git" / "incr_rm.txt"
    lr.write_bytes(b"\0".join(x.encode("utf-8") for x in sair))
    g("rm", "--cached", "-q", "--ignore-unmatch", "--pathspec-from-file=" + str(lr), "--pathspec-file-nul")
st = g("diff", "--cached", "--name-status").stdout.splitlines()
n_a = sum(1 for l in st if l.startswith("A")); n_m = sum(1 for l in st if l.startswith("M")); n_d = sum(1 for l in st if l.startswith("D"))
if COBERTO is not None:
    entra = {x for x in g("diff", "--cached", "--name-only", "-z", "--diff-filter=AM").stdout.split("\0") if x}
    sem = sorted(entra - COBERTO - {"README.md", "PATENTES.md", "vinculo_patentario.json"} - set(RAIZ_GERADA))
    if sem:
        g("reset", "-q")
        raise SystemExit("arquivos no commit sem conferência (%d): %s — nada publicado" % (len(sem), sem[:8]))
print("%s: no stage A %d / M %d / D %d" % (NOME, n_a, n_m, n_d))
resto = [l for l in g("status", "--porcelain", "--untracked-files=all").stdout.splitlines() if l and not l.startswith(("A ", "M ", "D ", "R "))]
if resto:
    print("  fora do stage (não entram; ditos):", len(resto), resto[:5])
if not st:
    print("nada a publicar"); sys.exit(0)
msg = ("%s\n\nCustódia v396 (22/10/2026): a mesma esteira da abertura (guarda pública, máscara visível, filtro das notas, regra do Escritório), "
       "em rodada incremental; conferência independente aprovada antes do envio. Acrescentados %d, alterados %d, retirados %d.\n\n%s\n"
       % (TIT, n_a, n_m, n_d, CO))
(D / ".git" / "msg_incr.txt").write_text(msg, encoding="utf-8")
g("commit", "-q", "-F", str(D / ".git" / "msg_incr.txt"))
t0 = time.time()
r = g("push", "origin", "main", ok=False)
if r.returncode != 0:
    time.sleep(30)
    r = g("push", "origin", "main", ok=False)
    assert r.returncode == 0, ("push falhou", r.stderr[-800:])
loc = g("rev-parse", "HEAD").stdout.strip()
g("fetch", "-q", "origin")
rem = g("rev-parse", "origin/main").stdout.strip()
arv = [x for x in g("ls-tree", "-r", "-z", "--name-only", "origin/main").stdout.split("\0") if x]
print("%s: HEAD %s = origin/main %s | árvore remota %d arquivos (índice %d + raiz %d) | push %.0f s" % (
    NOME, loc[:8], rem[:8], len(arv), len(idx), len(raiz), time.time() - t0))
assert loc == rem and set(arv) == quer, ("a árvore remota não é o índice", len(arv), len(quer))
print("PUBLICADO E CONFERIDO")
