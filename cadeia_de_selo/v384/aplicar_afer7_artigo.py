# -*- coding: utf-8 -*-
"""7a afericao nos trechos do artigo (PT/EN): a AUSENCIA da referencia na CPU so com o codigo CPUREF_JSON_ABSENT; qualquer outro erro: «a comparacao com a CPU
falhou (<erro>)» / «the CPU comparison failed (<error>)», sem afirmar ausencia. Backup ja feito (.bak_antes_afer7)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
PT = (r'''(r"A referência na CPU \textbf{não estava presente} nesta rodada ("
                  + (r"o arquivo \texttt{cpuref.json} não foi gravado" if _cr4.get("error_code") == "CPUREF_JSON_ABSENT" else (r"\texttt{" + _tx4(_cr4.get("error")) + r"}")) + r"); o processo da CPU "''',
      r'''(((r"A referência na CPU \textbf{não estava presente} nesta rodada (o arquivo \texttt{cpuref.json} não foi gravado)") if _cr4.get("error_code") == "CPUREF_JSON_ABSENT"
                    else (r"A comparação com a CPU \textbf{falhou} nesta rodada (\texttt{" + _tx4(_cr4.get("error")) + r"})")) + r"; o processo da CPU "''')
EN = (r'''(r"The CPU reference \textbf{was not present} in this run ("
                  + (r"the reference file \texttt{cpuref.json} was not written" if _cr4.get("error_code") == "CPUREF_JSON_ABSENT" else (r"\texttt{" + _tx4(_cr4.get("error")) + r"}")) + r"); the CPU process "''',
      r'''(((r"The CPU reference \textbf{was not present} in this run (the reference file \texttt{cpuref.json} was not written)") if _cr4.get("error_code") == "CPUREF_JSON_ABSENT"
                    else (r"The CPU comparison \textbf{failed} in this run (\texttt{" + _tx4(_cr4.get("error")) + r"})")) + r"; the CPU process "''')
for fn, (old, new) in (("artigo_pt_v384.pysnip", PT), ("artigo_en_v384.pysnip", EN)):
    p = os.path.join(HERE, fn); raw = open(p, "rb").read(); s = raw.decode("utf-8")
    assert open(p + ".bak_antes_afer7", "rb").read() == raw
    assert s.count(old) == 1, (fn, s.count(old))
    s = s.replace(old, new); b = s.encode("utf-8")
    open(p + ".tmp", "wb").write(b); os.replace(p + ".tmp", p); print("ok", fn)
