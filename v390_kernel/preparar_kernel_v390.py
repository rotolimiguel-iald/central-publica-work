# -*- coding: utf-8 -*-
"""preparar_kernel_v390.py -- prepara o SANDBOX (work\\v388_kernel\\kernel_src; nunca o kernel do Nos) para a v390: guarda os ANTES (bytes) das duas costuras,
copia a pedra Fundacao.lean (sha256 pinado pela ordem v390), +1 import no agregador TGLExt.lean, +9 #print axioms no TGL/Audit.lean. Idempotente; temporario -> replace."""
import hashlib, os, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
KS = os.path.join(os.path.dirname(HERE), "v388_kernel", "kernel_src")
NOS_K = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós", "tgl_kernel")
SRC = os.path.join(os.path.dirname(HERE), "superposicao_passagem_07out", "Fundacao.lean")
PIN = "66332d58fd216317ec5196a64a7aa670c87dcaa5edc59f57a5506bc621d3e073"
NOMES = ["nothing_above_bears_a_post", "the_climb_has_no_top", "the_climb_is_unbounded", "the_fall_never_lands", "abismo",
         "the_floor_fixes_the_cut", "agape", "agape_is_inhabited", "the_post_lives_in_the_passage"]
sha = lambda b: hashlib.sha256(b).hexdigest()
st = open(SRC, "rb").read(); assert sha(st) == PIN, "a pedra nao e a da ordem"
for rel, antes in (("TGLExt.lean", "TGLExt.lean.ANTES_v390"), (os.path.join("TGL", "Audit.lean"), "Audit.lean.ANTES_v390")):
    b = open(os.path.join(KS, rel), "rb").read(); a = os.path.join(HERE, antes)
    if not os.path.exists(a):
        assert b == open(os.path.join(NOS_K, rel), "rb").read(), "o sandbox nao bate com o Nos em %s" % rel
        open(a, "wb").write(b); assert open(a, "rb").read() == b
open(os.path.join(HERE, "AUDIT_NOMES_v390.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(NOMES) + "\n")
dst = os.path.join(KS, "TGLExt", "Fundacao.lean")
if not (os.path.exists(dst) and open(dst, "rb").read() == st):
    open(dst + ".tmp", "wb").write(st); os.replace(dst + ".tmp", dst)


def acrescenta(rel, extra, marca):
    p = os.path.join(KS, rel); b = open(p, "rb").read()
    if marca.encode() in b:
        print("ja esta:", rel); return
    nl = b"\r\n" if b"\r\n" in b else b"\n"
    novo = b.rstrip(b"\r\n") + nl + nl.join(x.encode("utf-8") for x in extra) + nl
    open(p + ".tmp", "wb").write(novo); assert open(p + ".tmp", "rb").read() == novo; os.replace(p + ".tmp", p); print("ok:", rel, len(b), "->", len(novo))


acrescenta("TGLExt.lean", ["import TGLExt.Fundacao"], "import TGLExt.Fundacao")
acrescenta(os.path.join("TGL", "Audit.lean"), ["-- 2026-10-07, v390: A FUNDACAO -- a superposicao e' a passagem; a clausula AGAPE (o fecho LOGICO do GLOBAL_LIFT, definicao do operador; recusa provada; passagem local [KNOWN])"]
           + ["#print axioms TGLExt.Fundacao.%s" % n for n in NOMES], "TGLExt.Fundacao.agape_is_inhabited")
print("pedra:", sha(open(dst, "rb").read())[:16])
