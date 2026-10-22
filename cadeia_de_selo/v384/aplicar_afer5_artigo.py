# -*- coding: utf-8 -*-
"""5a afericao nos trechos do artigo (PT/EN): a frase da referencia na CPU SO nos vereditos anulados pela CPU (NOT_COMPARABLE ou DISAGREES_OR_ABSENT, nunca no
sucesso, que contem CPU_REFERENCE_AGREES), dizendo a AUSENCIA quando a referencia faltou e o codigo do filho sem o «None» do Python; o veredito composto
PARTIAL+CUSTODY nao e' lido como parcial valido; a fracao do T1 truncada (nunca arredonda para 100). Backup ja feito (.bak_antes_afer5)."""
import os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PART_OLD = '''    _part4 = _succ4 and "__PARTIAL_RESULT_" in _v4'''
PART_NEW = '''    _part4 = _succ4 and "__PARTIAL_RESULT_" in _v4 and "__CUSTODY_CHAIN_INCOMPLETE__" not in _v4   # o composto PARCIAL+CUSTODY nao e' parcial valido (5a afericao)
    _cpuvoid4 = ("__CPU_REFERENCE_NOT_COMPARABLE__" in _v4 or "__CPU_REFERENCE_DISAGREES_OR_ABSENT__" in _v4)
    _crc4 = _cr4.get("child_rc")'''
PT = [
    (PART_OLD, PART_NEW),
    (r'''             + ((r"A referência na CPU, nesta rodada: leu " + _i4(_cr4.get("read")) + r" pontos, comparou " + _i4(_cr4.get("compared")) + r" (" + _i4(_cr4.get("near_threshold_not_compared")) + r" perto do limiar do gap), discordou em "
                 + _i4(_cr4.get("disagreements")) + r"; marca da rodada " + (r"conferida" if _cr4.get("meta_ok") else r"\textbf{não conferida}") + r"; código de saída do filho " + _tx4(_cr4.get("child_rc")) + r". ")
                if ("__CPU_REFERENCE_" in _v4 and _cr4) else "")''',
     r'''             + (((r"A referência na CPU \textbf{não estava presente} nesta rodada (" + (_tx4(_cr4.get("error")) if _cr4.get("error") else r"sem registro") + r"); o processo da CPU "
                  + ((r"terminou com código " + _tx4(_crc4)) if _crc4 is not None else r"não terminou ou foi encerrado pelo prazo") + r". ")
                 if (not _cr4 or _cr4.get("error")) else
                 (r"A referência na CPU, nesta rodada: leu " + _i4(_cr4.get("read")) + r" pontos, comparou " + _i4(_cr4.get("compared")) + r" (" + _i4(_cr4.get("near_threshold_not_compared")) + r" perto do limiar do gap), discordou em "
                  + _i4(_cr4.get("disagreements")) + (r"; a marca da rodada \textbf{não conferiu}" if _cr4.get("meta_ok") is False else "") + r"; o processo da CPU "
                  + ((r"terminou com código " + _tx4(_crc4)) if _crc4 is not None else r"não terminou ou foi encerrado pelo prazo") + r". "))
                if _cpuvoid4 else "")'''),
    (r'''((("%.1f" % (100.0 * f_)).replace(".", "{,}") + r"\% (" ''', r'''((("%.1f" % (int(1000.0 * f_) / 10.0)).replace(".", "{,}") + r"\% (" '''),
]
EN = [
    (PART_OLD, PART_NEW),
    (r'''             + ((r"The CPU reference, in this run: read " + _i4(_cr4.get("read")) + r" points, compared " + _i4(_cr4.get("compared")) + r" (" + _i4(_cr4.get("near_threshold_not_compared")) + r" near the gap threshold), disagreed in "
                 + _i4(_cr4.get("disagreements")) + r"; run mark " + (r"checked" if _cr4.get("meta_ok") else r"\textbf{not checked}") + r"; child exit code " + _tx4(_cr4.get("child_rc")) + r". ")
                if ("__CPU_REFERENCE_" in _v4 and _cr4) else "")''',
     r'''             + (((r"The CPU reference \textbf{was not present} in this run (" + (_tx4(_cr4.get("error")) if _cr4.get("error") else r"no record") + r"); the CPU process "
                  + ((r"ended with code " + _tx4(_crc4)) if _crc4 is not None else r"did not finish or was stopped at the deadline") + r". ")
                 if (not _cr4 or _cr4.get("error")) else
                 (r"The CPU reference, in this run: read " + _i4(_cr4.get("read")) + r" points, compared " + _i4(_cr4.get("compared")) + r" (" + _i4(_cr4.get("near_threshold_not_compared")) + r" near the gap threshold), disagreed in "
                  + _i4(_cr4.get("disagreements")) + (r"; the run mark \textbf{did not check}" if _cr4.get("meta_ok") is False else "") + r"; the CPU process "
                  + ((r"ended with code " + _tx4(_crc4)) if _crc4 is not None else r"did not finish or was stopped at the deadline") + r". "))
                if _cpuvoid4 else "")'''),
    (r'''((("%.1f" % (100.0 * f_)) + r"\% (" ''', r'''((("%.1f" % (int(1000.0 * f_) / 10.0)) + r"\% (" '''),
]
for fn, pairs in (("artigo_pt_v384.pysnip", PT), ("artigo_en_v384.pysnip", EN)):
    p = os.path.join(HERE, fn); raw = open(p, "rb").read(); s = raw.decode("utf-8")
    assert open(p + ".bak_antes_afer5", "rb").read() == raw
    for old, new in pairs:
        c = s.count(old); assert c == 1, (fn, c, old[:140])
        s = s.replace(old, new)
    b = s.encode("utf-8"); open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)
    print("ok", fn, len(pairs))
