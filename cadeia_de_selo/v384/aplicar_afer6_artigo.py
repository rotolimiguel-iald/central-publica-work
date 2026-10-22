# -*- coding: utf-8 -*-
"""6a afericao nos trechos do artigo (PT/EN): com o resumo falho, a frase da CPU nao afirma ausencia (o resumo vazio nao e' ausencia); sem registro da comparacao
diz so isso; a ausencia composta a partir do CODIGO (CPUREF_JSON_ABSENT) em cada lingua; «nao conferiu»/«did not check» -> «nao bateu»/«did not match».
Backup ja feito (.bak_antes_afer6)."""
import os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PT = [
    (r'''             + (((r"A referência na CPU \textbf{não estava presente} nesta rodada (" + (_tx4(_cr4.get("error")) if _cr4.get("error") else r"sem registro") + r"); o processo da CPU "''',
     r'''             + (((r"Não há registro da comparação com a CPU nesta rodada. ") if not _cr4 else (r"A referência na CPU \textbf{não estava presente} nesta rodada ("
                  + (r"o arquivo \texttt{cpuref.json} não foi gravado" if _cr4.get("error_code") == "CPUREF_JSON_ABSENT" else (r"\texttt{" + _tx4(_cr4.get("error")) + r"}")) + r"); o processo da CPU "'''),
    (r'''r"não terminou ou foi encerrado pelo prazo") + r". ")
                 if (not _cr4 or _cr4.get("error")) else''', r'''r"não terminou ou foi encerrado pelo prazo") + r". "))
                 if (not _cr4 or _cr4.get("error")) else'''),
    (r'''\textbf{não conferiu}''', r'''\textbf{não bateu}'''),
    (r'''                if _cpuvoid4 else "")''', r'''                if (_cpuvoid4 and not _q4.get("summary_error")) else "")   # o resumo vazio nao e' ausencia (6a afericao)'''),
]
EN = [
    (r'''             + (((r"The CPU reference \textbf{was not present} in this run (" + (_tx4(_cr4.get("error")) if _cr4.get("error") else r"no record") + r"); the CPU process "''',
     r'''             + (((r"There is no record of the CPU comparison in this run. ") if not _cr4 else (r"The CPU reference \textbf{was not present} in this run ("
                  + (r"the reference file \texttt{cpuref.json} was not written" if _cr4.get("error_code") == "CPUREF_JSON_ABSENT" else (r"\texttt{" + _tx4(_cr4.get("error")) + r"}")) + r"); the CPU process "'''),
    (r'''r"did not finish or was stopped at the deadline") + r". ")
                 if (not _cr4 or _cr4.get("error")) else''', r'''r"did not finish or was stopped at the deadline") + r". "))
                 if (not _cr4 or _cr4.get("error")) else'''),
    (r'''\textbf{did not check}''', r'''\textbf{did not match}'''),
    (r'''                if _cpuvoid4 else "")''', r'''                if (_cpuvoid4 and not _q4.get("summary_error")) else "")   # an empty summary is not absence (6th audit)'''),
]
for fn, pairs in (("artigo_pt_v384.pysnip", PT), ("artigo_en_v384.pysnip", EN)):
    p = os.path.join(HERE, fn); raw = open(p, "rb").read(); s = raw.decode("utf-8")
    assert open(p + ".bak_antes_afer6", "rb").read() == raw
    for old, new in pairs:
        c = s.count(old); assert c == 1, (fn, c, old[:140])
        s = s.replace(old, new)
    b = s.encode("utf-8"); open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)
    print("ok", fn, len(pairs))
