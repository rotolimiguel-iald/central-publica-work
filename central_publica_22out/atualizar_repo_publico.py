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
               "llms.txt",   # (23/10/2026) o mapa de máquina de cada repositório, curadoria à mão do Kimi: rastreado, fora do índice
               "RECONSTRUIR_COPIAS.py"]   # (11/11/2026) recria num clone as cópias referenciadas (copias_referencia.py)


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
_todas = json.loads((D / "INDICE_PUBLICO.json").read_text(encoding="utf-8"))["arquivos"]
# AO LADO (11/11/2026, claude-site-custodia; decisão do operador: a cópia vira referência, a partir da v411): a entrada com "igual_a" é uma
# cópia idêntica de outro arquivo do índice; ela fica no índice e NÃO vai ao git (sai da árvore, se estava). A conferência do delta já
# conferiu cada referência contra o original; aqui só se exige que o script que as recria esteja na raiz.
idx = [a["caminho"] for a in _todas if not a.get("igual_a")]
n_refs = len(_todas) - len(idx)
assert not n_refs or (D / "RECONSTRUIR_COPIAS.py").is_file(), "cópias referenciadas sem RECONSTRUIR_COPIAS.py na raiz — PARAR"
raiz = [n for n in RAIZ_GERADA if (D / n).is_file()]
# AO LADO (11/11/2026, custódia v410, claude-site-custodia): o índice EM PARTES (indice_partes.py). Com INDICE_PUBLICO_PARTES/PARTES.json no
# preparo, o git leva as partes e o cabeçalho, e o índice inteiro (acima do teto de arquivo do GitHub) sai do git e fica local; a conferência
# do delta já conferiu as partes contra o índice. O índice inteiro TEM de estar fora do git (.git/info/exclude), senão PARAR.
PARTES_CAB = D / "INDICE_PUBLICO_PARTES" / "PARTES.json"
if PARTES_CAB.is_file():
    _env_ci = {k: v for k, v in os.environ.items() if k != "GIT_LITERAL_PATHSPECS"}   # check-ignore recusa a magia 'literal' (rc 128)
    assert subprocess.run(["git", "-C", str(D), "check-ignore", "-q", "INDICE_PUBLICO.json"], capture_output=True, env=_env_ci).returncode == 0, \
        "índice em partes, mas o inteiro não está fora do git — PARAR"
    cab_p = json.loads(PARTES_CAB.read_text(encoding="utf-8"))
    assert cab_p.get("entradas") == len(_todas), ("PARTES.json não tem as entradas do índice — PARAR", cab_p.get("entradas"), len(_todas))
    pts = ["INDICE_PUBLICO_PARTES/PARTES.json"] + [p["arquivo"] for p in cab_p["partes"]]
    assert all((D / p).is_file() for p in pts), "parte listada ausente — PARAR"
    raiz = [n for n in raiz if n != "INDICE_PUBLICO.json"] + pts   # as partes NÃO entram na isenção da raiz: a conferência do delta tem de cobri-las
quer = set(idx) | set(raiz)
tem = set(x for x in g("ls-files", "-z").stdout.split("\0") if x)
sair = sorted(tem - quer)
lista = D / ".git" / "incr_add.txt"
# AO LADO (12/11/2026, claude-site-custodia; de acordo da gerencia c1): o add vai so com o que difere do HEAD, nao com o indice inteiro.
# O add de sorted(quer) (560.887 caminhos no work) ficou 3.917 s sem escrever o index.lock na publicacao do pre-registro do H0DN e e o
# passo das 14.322 s do C18 da v410; o do delta levou 1 s. O stage e o mesmo: entram os caminhos do indice que o git nao rastreia
# (o -f fica: o .gitignore copiado da origem nao barra o curado) e os rastreados que o status mostra mudados. Antes:
#   lista.write_bytes(b"\0".join(x.encode("utf-8") for x in sorted(quer))); g("add", "-f", "--pathspec-from-file=" + str(lista), ...)
_tok = g("status", "--porcelain", "-z", "--untracked-files=all").stdout.split("\0")
_mud, _i = set(), 0
while _i < len(_tok):
    _e = _tok[_i]; _i += 1
    if len(_e) > 3:
        _mud.add(_e[3:])
        if _e[0] in "RC":
            _i += 1   # com -z, o nome de origem de um rename vem no token seguinte, sem o prefixo XY
_dif = sorted((quer - tem) | (_mud & quer))
lista.write_bytes(b"\0".join(x.encode("utf-8") for x in _dif))
if _dif:
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
       "em rodada incremental; conferência independente aprovada antes do envio. Acrescentados %d, alterados %d, retirados %d.\n%s\n%s\n"
       % (TIT, n_a, n_m, n_d, ("Cópias idênticas só no índice, com o original em igual_a (decisão do operador de 11/11/2026; "
                               "RECONSTRUIR_COPIAS.py as recria num clone): %d.\n" % n_refs) if n_refs else "", CO))
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
print("%s: HEAD %s = origin/main %s | árvore remota %d arquivos (índice %d + raiz %d; %d cópias só no índice) | push %.0f s" % (
    NOME, loc[:8], rem[:8], len(arv), len(idx), len(raiz), n_refs, time.time() - t0))
assert loc == rem and set(arv) == quer, ("a árvore remota não é o índice", len(arv), len(quer))
print("PUBLICADO E CONFERIDO")
