# -*- coding: utf-8 -*-
"""preparar_kernel_v392.py -- prepara o kernel do SANDBOX C:\\t\\k392 (nunca o do Nos) para a v392. Molde: preparar_kernel_v390.py.
fases:
  explorar : (sandbox A = C:\\t\\k392\\kernel) guarda os ANTES (bytes), copia as pedras de STONES (14 na rodada 2; pinos lidos por script), +1 import por pedra na raiz TGLExt.lean.
             Depois disso: lake build, enumeracao COB (Cob_v392.lean), gerar_audit_v392.py.
  final    : (sandbox B = C:\\t\\k392\\final, copia NOVA do kernel de partida) todas as pedras de STONES + a raiz + o Audit final (bloco gerado na exploracao) => UM unico
             lake build compila tudo (o contrato do recibo do kernel exige as linhas Built de cada pedra, da raiz e do Audit no MESMO build).
Idempotente por fase; temporario -> conferir -> replace. Uso: python -I -B -X utf8 preparar_kernel_v392.py explorar|final"""
import hashlib, os, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import v392_pedras as P  # noqa: E402
KD = os.path.join(HERE, "kernel"); os.makedirs(KD, exist_ok=True)
NK = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós", "tgl_kernel")
SA = os.path.join("C:" + os.sep, "t", "k392", "kernel"); SB = os.path.join("C:" + os.sep, "t", "k392", "final")
sha = lambda b: hashlib.sha256(b).hexdigest()
fase = sys.argv[1]
K = SA if fase == "explorar" else SB
assert fase in ("explorar", "final")
assert os.path.isdir(K), "sandbox ausente: " + K
# 1) os ANTES (bytes), conferidos contra o Nos
for rel, antes in (("TGLExt.lean", "TGLExt.lean.ANTES_v392"), (os.path.join("TGL", "Audit.lean"), "Audit.lean.ANTES_v392")):
    b = open(os.path.join(NK, rel), "rb").read(); a = os.path.join(KD, antes)
    if not os.path.exists(a):
        open(a, "wb").write(b); assert open(a, "rb").read() == b
    assert open(a, "rb").read() == b, "o ANTES gravado nao e' o que o Nos tem agora"
    if not os.path.exists(os.path.join(K, "TGLExt", "Palavra.lean")):   # primeira vez nesta copia: ela tem de ser a v391 do Nos
        assert open(os.path.join(K, rel), "rb").read() == b, "o sandbox de partida nao bate com o Nos em " + rel
# 2) as pedras (bytes pinados por script)
pins = P.gerar_pinos(); assert all(p["confere_com_a_entrega"] for p in pins)
for s, p in zip(P.STONES, pins):
    b = P.bytes_da_pedra(s); assert sha(b) == p["sha256"]
    dst = os.path.join(K, "TGLExt", s["mod"] + ".lean")
    assert not os.path.exists(os.path.join(NK, "TGLExt", s["mod"] + ".lean")), "a pedra ja esta no kernel do Nos: " + s["mod"]
    if not (os.path.exists(dst) and open(dst, "rb").read() == b):
        open(dst + ".tmp", "wb").write(b); assert open(dst + ".tmp", "rb").read() == b; os.replace(dst + ".tmp", dst)


def acrescenta(rel, linhas, marca):
    p = os.path.join(K, rel); b = open(p, "rb").read()
    if marca.encode() in b:
        print("ja esta:", rel); return
    nl = b"\r\n" if b"\r\n" in b else b"\n"
    novo = b.rstrip(b"\r\n") + nl + nl.join(x.encode("utf-8") for x in linhas) + nl
    open(p + ".tmp", "wb").write(novo); assert open(p + ".tmp", "rb").read() == novo; os.replace(p + ".tmp", p); print("ok:", rel, len(b), "->", len(novo))


# 3) a raiz: +1 import por pedra (len(STONES)), na ordem de instalacao
acrescenta("TGLExt.lean", ["import TGLExt.%s" % s["mod"] for s in P.STONES], "import TGLExt.%s" % P.STONES[-1]["mod"])
if fase == "final":
    bloco = os.path.join(KD, "AUDIT_BLOCO_v392.txt"); assert os.path.exists(bloco), "rode a fase explorar + gerar_audit_v392.py antes"
    linhas = open(bloco, encoding="utf-8").read().rstrip("\n").split("\n")
    acrescenta(os.path.join("TGL", "Audit.lean"), linhas, linhas[-1])
print("fase", fase, "pronta; raiz", sha(open(os.path.join(K, "TGLExt.lean"), "rb").read())[:16], "audit", sha(open(os.path.join(K, "TGL", "Audit.lean"), "rb").read())[:16])
