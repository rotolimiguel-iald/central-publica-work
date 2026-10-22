# -*- coding: utf-8 -*-
"""Pós-push da custódia v393+v394 (19/10/2026, sessão a7): os hashes dos dois commits (LIDOS do git) e a conferência final independente nas
memórias de fora do repositório (handoff, estado da Central, diário do site) e na linha do MEMORY.md (a antiga VERBATIM no MEMORY_2.md).
O Atlas (dentro do repo da Central) já tem o bloco da custódia; não se toca aqui para não deixar a árvore suja depois do push."""
import json, os, subprocess, sys
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")
TS = datetime.now().strftime("%Y%m%d_%H%M%S")
AGORA = datetime.now().strftime("%d/%m/%Y %H:%M")
MEM = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"
W = r"C:\IALD\Central de Patentes\work\custodia_v394_19out"


def git(repo, *a):
    return subprocess.run(["git", "-C", repo] + list(a), capture_output=True, text=True).stdout.strip()


def tocar(p, f, pode_encolher=False):
    raw = open(p, "rb").read()
    open(p + ".bak_" + TS, "wb").write(raw)
    nl = "\r\n" if b"\r\n" in raw else "\n"
    novo = f(raw.decode("utf-8"), nl).encode("utf-8")
    tmp = p + ".tmp_" + TS
    open(tmp, "wb").write(novo)
    assert pode_encolher or os.path.getsize(tmp) > len(raw), p
    os.replace(tmp, p)
    print("ok", os.path.basename(p), len(raw), "->", os.path.getsize(p))


def ap(p, texto):
    tocar(p, lambda t, nl: t.rstrip("\r\n") + nl + nl + texto.strip("\n").replace("\n", nl) + nl)


TB, CEN = r"C:\IALD\Artigo\the_boundary", r"C:\IALD\Central de Patentes"
esp, esp_o = git(TB, "rev-parse", "--short", "HEAD"), git(TB, "rev-parse", "--short", "origin/main")
cen, cen_o = git(CEN, "rev-parse", "--short=8", "HEAD"), git(CEN, "rev-parse", "--short=8", "origin/main")
assert esp == esp_o and cen == cen_o, (esp, esp_o, cen, cen_o)
cf = json.load(open(os.path.join(W, "CONFERENCIA_FINAL_v394.json"), encoding="utf-8"))
assert cf["ok"] == cf["total"] == 12, (cf["ok"], cf["total"])
TXT = ("PUBLICADA. Espelho the_boundary `%s` = origin/main; Central `%s` = origin/main (privado); site no ar. Conferência final independente "
       "(`work/custodia_v394_19out/conferencia_final_v394.py`, sem importar a esteira): **%d/%d ok** — o um.py igual no Nós, no espelho, no cofre e no "
       "raw do GitHub (o pino); o cofre e o kernel (1423 formais; 29026 declarações no trio) conferem; o site no ar e o README raw trazem o pino; "
       "os dois repositórios sem nada pendente nos caminhos da custódia. PCT: o Codex ficou sem créditos; a Central fechou os controles da ENTREGA_009 "
       "(26/11 nos marcos; auditoria +2 processos; anuidade 6 meses; REVISAO_012). O gate não se moveu." % (esp, cen, cf["ok"], cf["total"]))
ap(os.path.join(MEM, "handoff-v394-custodia.md"), "## %s — PUBLICADA (pós-push)\n\n%s" % (AGORA, TXT))
ap(os.path.join(MEM, "central-de-patentes-estado.md"), "## %s — custódia v394 publicada\n\n%s" % (AGORA, TXT))
ap(r"C:\IALD\Site\tgl\v3.0_bancada\DIARIO_DO_SITE.md", "## %s — a custódia v393+v394 PUBLICADA\n\n%s" % (AGORA, TXT))
M, M2 = os.path.join(MEM, "MEMORY.md"), os.path.join(MEM, "MEMORY_2.md")
t = open(M, "rb").read().decode("utf-8")
nl = "\r\n" if "\r\n" in t else "\n"
old = [l for l in t.split(nl) if l.startswith("- [HANDOFF v394 — o relógio M2, a rede de Fock e as cunhagens; custódia](handoff-v394-custodia.md)")]
assert len(old) == 1, old
nova = ("- [HANDOFF v394 — o relógio M2, a rede de Fock e as cunhagens; custódia](handoff-v394-custodia.md) — **19/10: PUBLICADA com a v393** "
        "(the_boundary `%s`; Central `%s`; site no ar; cofre v394, runner v59, 16/16, FINAL, ledger 0; conferência final %d/%d) · `972e81f22dd8cc68`"
        % (esp, cen, cf["ok"], cf["total"]))
ap(M2, "## %s — linha movida do MEMORY.md (regra dos dois arquivos), VERBATIM\n\n%s" % (AGORA, old[0]))
tocar(M, lambda t_, nl_: t_.replace(old[0], nova, 1), pode_encolher=True)
assert os.path.getsize(M) < 24 * 1024, os.path.getsize(M)
print("PUBLICADA:", esp, cen, "%d/%d" % (cf["ok"], cf["total"]))
