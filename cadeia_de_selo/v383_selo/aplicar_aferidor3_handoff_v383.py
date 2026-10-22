# -*- coding: utf-8 -*-
"""3a passada do aferidor, B-2/B-3: o handoff_v383 confere ANTES da primeira gravacao (1) que os dois AFERIDOR arquivados existem e (2) que o MEMORY.md
comporta a linha do handoff E a marca DECIDIDO; se nao, recusa sem gravar nada. A definicao de `linha` sobe para antes das gravacoes (o texto nao muda)."""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(HERE, "handoff_v383.py")
raw = open(P, "rb").read(); bak = P + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_afer3"; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
s = raw.decode("utf-8"); L = s.split("\n")
ks = [i for i, l in enumerate(L) if l.startswith('linha = ("- [HANDOFF v383 ')]
assert len(ks) == 1; LINHA = L.pop(ks[0])
ka = [i for i, l in enumerate(L) if l.startswith('STAMP = time.strftime(')]
assert len(ka) == 1
PRE = [
    "# v383 (aferidor, 3a passada, B-2/B-3): conferir ANTES da primeira gravacao -- os dois AFERIDOR arquivados existem e o indice comporta a linha do handoff E a marca DECIDIDO",
    '_ARQ = r"C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo"',
    'for _f in (os.path.join(_ARQ, "v383", "AFERIDOR_v383.txt"), os.path.join(_ARQ, "v382", "AFERIDOR_v382.txt")):',
    "    if not os.path.exists(_f):",
    '        print("HANDOFF RECUSADO (nada gravado): o arquivo de afericao arquivado nao existe -- rode o arquivar antes:", _f); sys.exit(2)',
    LINHA,
    '_raw0 = open(os.path.join(UMEM, "MEMORY.md"), "rb").read()',
    'if b"handoff-v383-custodia.md" not in _raw0:',
    '    _dec = " · **%s: DECIDIDO — a v383 `%s` supera; a v382 fica só no Nós**" % (V["data"][:5], V["s16"])',
    '    _need = len(_raw0) + len((linha + "\\n").encode("utf-8")) + len(_dec.encode("utf-8"))',
    "    if _need > 24000:",
    '        print("HANDOFF RECUSADO (nada gravado): o indice ficaria com %d B > 24 000 com a linha e a marca DECIDIDO -- liberar folga (regra dos dois arquivos) e rerodar" % _need); sys.exit(3)',
    '    print("pre-conferencia: o indice ficara com %d B (limite 24 000)" % _need)',
]
L[ka[0]:ka[0]] = PRE
s2 = "\n".join(L); ast.parse(s2)
assert s2.count('linha = ("- [HANDOFF v383 ') == 1 and s2.index('linha = ("- [HANDOFF v383 ') < s2.index('p = os.path.join(UMEM, "handoff-v383-custodia.md")')
open(P + ".tmp", "w", encoding="utf-8", newline="").write(s2); os.replace(P + ".tmp", P); print("ok", P)
