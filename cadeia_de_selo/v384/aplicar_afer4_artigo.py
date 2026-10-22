# -*- coding: utf-8 -*-
"""4a afericao nos trechos do artigo (PT/EN em paridade): _tx4 so ASCII; a fracao do T1 sem ruido dita por dimensao (k de n) quando nao e' 100%; a frase das
janelas sem o parentese que prometia um intervalo nao relatado; a contagem do motor diz «nao resumido» quando o resumo falhou; o hash do pre-registro separa a
ESPECIFICACAO do DOCUMENTO (JSON e MD); a referencia na CPU dita nos vereditos RESULTS_VOID com CPU_REFERENCE_ (o ramo morto do _cpu4 removido).
Backup ja feito (.bak_antes_afer4)."""
import os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TX_OLD = r'''    _tx4 = lambda x_: "".join(c_ if (c_.isalnum() or c_ in " .,:;()'=<>/+-") else (r"\_" if c_ == "_" else "?") for c_ in str(x_)[:200])   # so caracteres seguros (PDF e TXT)'''
TX_NEW = r'''    _tx4 = lambda x_: "".join(c_ if ((c_.isascii() and c_.isalnum()) or c_ in " .,:;()'=<>/+-") else (r"\_" if c_ == "_" else "?") for c_ in str(x_)[:200])   # so ASCII seguro (PDF e TXT; 4a afericao)
    _p0d4 = sorted(((d_, v_.get("pass_sigma0"), v_.get("n")) for d_, v_ in (_t1.get("per_d") or {}).items()), key=lambda t_: int(t_[0]) if str(t_[0]).isdigit() else 0)
    _pf4 = _q4.get("preregistration") or {}; _pff4 = _pf4.get("files") or {}'''
COMMON_CPU_OLD_PT = r'''        _cpu4 = (r"concorda" if _cr4.get("ok") else (r"\textbf{não estava presente}" if (not _cr4 or _cr4.get("error")) else (r"\textbf{não é desta rodada ou não terminou}" if (_cr4.get("meta_ok") is False or _cr4.get("child_rc") not in (0, None))
                 else (r"\textbf{não pôde comparar nenhum ponto} (todos perto do limiar do gap: nem discordância, nem conferência)" if _cr4.get("not_comparable") else r"\textbf{discorda}"))))'''
COMMON_CPU_NEW_PT = r'''        _cpu4 = r"concorda" if _cr4.get("ok") else r"\textbf{não concorda}"   # aqui o veredito e' de sucesso, que exige a CPU de acordo; o caso contrario e' dito com o RESULTS_VOID'''
COMMON_CPU_OLD_EN = r'''        _cpu4 = (r"agrees" if _cr4.get("ok") else (r"\textbf{was not present}" if (not _cr4 or _cr4.get("error")) else (r"\textbf{is not from this run or did not finish}" if (_cr4.get("meta_ok") is False or _cr4.get("child_rc") not in (0, None))
                 else (r"\textbf{could not compare any point} (all near the gap threshold: neither disagreement nor check)" if _cr4.get("not_comparable") else r"\textbf{disagrees}"))))'''
COMMON_CPU_NEW_EN = r'''        _cpu4 = r"agrees" if _cr4.get("ok") else r"\textbf{does not agree}"   # here the verdict is a success, which requires the CPU to agree; otherwise it is said with RESULTS_VOID'''
PT = [
    (TX_OLD, TX_NEW), (COMMON_CPU_OLD_PT, COMMON_CPU_NEW_PT),
    (r'''             + ((r"\textbf{Os números desta rodada não puderam ser resumidos para o artigo} (\texttt{" + _tx4(_q4.get("summary_error")) + r"}); o veredito e o resultado estão no selo e em \texttt{um\_absoluto\_pilar\_quantico.json}. ") if _q4.get("summary_error") else "")''',
     r'''             + ((r"\textbf{Os números desta rodada não puderam ser resumidos para o artigo} (\texttt{" + _tx4(_q4.get("summary_error")) + r"}); o veredito e o resultado estão no selo e em \texttt{um\_absoluto\_pilar\_quantico.json}. ") if _q4.get("summary_error") else "")
             + ((r"A referência na CPU, nesta rodada: leu " + _i4(_cr4.get("read")) + r" pontos, comparou " + _i4(_cr4.get("compared")) + r" (" + _i4(_cr4.get("near_threshold_not_compared")) + r" perto do limiar do gap), discordou em "
                 + _i4(_cr4.get("disagreements")) + r"; marca da rodada " + (r"conferida" if _cr4.get("meta_ok") else r"\textbf{não conferida}") + r"; código de saída do filho " + _tx4(_cr4.get("child_rc")) + r". ")
                if ("__CPU_REFERENCE_" in _v4 and _cr4) else "")'''),
    (r'''if _eng4 else r"sem registro nesta rodada."))''', r'''if _eng4 else (r"não resumido nesta rodada (ver acima)." if _q4.get("summary_error") else r"sem registro nesta rodada.")))'''),
    (r'''r"); há ao menos um ponto de atrator único da grade (os pontos não precisam ser contíguos) em que o atrator guarda ao menos metade do peso em $\Pi$ em " + _i4(_t2.get("name_in_core_configs")) + r" das " + _i4(_t2.get("configs")) +
                 r" configurações, e um com as dobras $n(c^1)\in[2{,}5;\,3{,}5]$ e $n(c^2)\in[1{,}5;\,2{,}5]$ --- na prática, quase-pureza do atrator --- em " + _i4(_t2.get("folds_window_configs")) + r" das " + _i4(_t2.get("configs")) + r". "''',
     r'''r"); em " + _i4(_t2.get("name_in_core_configs")) + r" das " + _i4(_t2.get("configs")) + r" configurações há ao menos um ponto de atrator único da grade em que o atrator guarda ao menos metade do peso em $\Pi$, "
                 r"e em " + _i4(_t2.get("folds_window_configs")) + r" das " + _i4(_t2.get("configs")) + r" há um com as dobras $n(c^1)\in[2{,}5;\,3{,}5]$ e $n(c^2)\in[1{,}5;\,2{,}5]$ --- na prática, quase-pureza do atrator. "'''),
    (r'''r"sem ruído, recupera os dois em " + ("100\\%" if (_p0_4 and all(x_ == 1.0 for x_ in _p0_4)) else ("menos de 100\\%" if _p0_4 else "n/d")) + r" das injeções;''',
     r'''r"sem ruído, recupera os dois em " + ("100\\% das injeções" if (_p0_4 and all(x_ == 1.0 for x_ in _p0_4)) else (("uma fração das injeções, por dimensão: " + ", ".join(r"$d=" + str(d_) + r"$: " + ((("%.1f" % (100.0 * f_)).replace(".", "{,}") + r"\% (" + str(int(round(f_ * n_))) + r" de " + str(n_) + ")") if (_fin4(f_) and _fin4(n_)) else "n/d") for d_, f_, n_ in _p0d4)) if _p0_4 else "n/d")) + r";''' ),
    (r'''             r"O pré-registro está congelado por hash (\texttt{" + _tt4(str(_q4.get("preregistration", {}).get("spec_sha256", "n/d"))[:16]) + r"}); o gate não muda."''',
     r'''             r"A especificação do pré-registro está congelada por hash (\texttt{" + _tt4(str(_pf4.get("spec_sha256", "n/d"))[:16]) + r"}); o documento, por \texttt{" + _tt4(str((_pff4.get("json") or {}).get("sha256", "n/d"))[:16])
             + r"} (JSON) e \texttt{" + _tt4(str((_pff4.get("md") or {}).get("sha256", "n/d"))[:16]) + r"} (MD); o gate não muda."'''),
]
EN = [
    (TX_OLD, TX_NEW), (COMMON_CPU_OLD_EN, COMMON_CPU_NEW_EN),
    (r'''             + ((r"\textbf{This run's numbers could not be summarized for the article} (\texttt{" + _tx4(_q4.get("summary_error")) + r"}); the verdict and the result are in the seal and in \texttt{um\_absoluto\_pilar\_quantico.json}. ") if _q4.get("summary_error") else "")''',
     r'''             + ((r"\textbf{This run's numbers could not be summarized for the article} (\texttt{" + _tx4(_q4.get("summary_error")) + r"}); the verdict and the result are in the seal and in \texttt{um\_absoluto\_pilar\_quantico.json}. ") if _q4.get("summary_error") else "")
             + ((r"The CPU reference, in this run: read " + _i4(_cr4.get("read")) + r" points, compared " + _i4(_cr4.get("compared")) + r" (" + _i4(_cr4.get("near_threshold_not_compared")) + r" near the gap threshold), disagreed in "
                 + _i4(_cr4.get("disagreements")) + r"; run mark " + (r"checked" if _cr4.get("meta_ok") else r"\textbf{not checked}") + r"; child exit code " + _tx4(_cr4.get("child_rc")) + r". ")
                if ("__CPU_REFERENCE_" in _v4 and _cr4) else "")'''),
    (r'''if _eng4 else r"no record in this run."))''', r'''if _eng4 else (r"not summarized in this run (see above)." if _q4.get("summary_error") else r"no record in this run.")))'''),
    (r'''r"); there is at least one grid point with a unique attractor (the points need not be contiguous) where the attractor keeps at least half of its weight in $\Pi$ in " + _i4(_t2.get("name_in_core_configs")) + r" of the " + _i4(_t2.get("configs")) +
                 r" configurations, and one with the folds $n(c^1)\in[2.5,\,3.5]$ and $n(c^2)\in[1.5,\,2.5]$ --- in practice, near-purity of the attractor --- in " + _i4(_t2.get("folds_window_configs")) + r" of the " + _i4(_t2.get("configs")) + r". "''',
     r'''r"); in " + _i4(_t2.get("name_in_core_configs")) + r" of the " + _i4(_t2.get("configs")) + r" configurations there is at least one grid point with a unique attractor where the attractor keeps at least half of its weight in $\Pi$, "
                 r"and in " + _i4(_t2.get("folds_window_configs")) + r" of the " + _i4(_t2.get("configs")) + r" there is one with the folds $n(c^1)\in[2.5,\,3.5]$ and $n(c^2)\in[1.5,\,2.5]$ --- in practice, near-purity of the attractor. "'''),
    (r'''r"without noise it recovers both in " + ("100\\%" if (_p0_4 and all(x_ == 1.0 for x_ in _p0_4)) else ("less than 100\\%" if _p0_4 else "n/a")) + r" of the injections;''',
     r'''r"without noise it recovers both in " + ("100\\% of the injections" if (_p0_4 and all(x_ == 1.0 for x_ in _p0_4)) else (("a fraction of the injections, per dimension: " + ", ".join(r"$d=" + str(d_) + r"$: " + ((("%.1f" % (100.0 * f_)) + r"\% (" + str(int(round(f_ * n_))) + r" of " + str(n_) + ")") if (_fin4(f_) and _fin4(n_)) else "n/a") for d_, f_, n_ in _p0d4)) if _p0_4 else "n/a")) + r";'''),
    (r'''             r"The pre-registration is frozen by hash (\texttt{" + _tt4(str(_q4.get("preregistration", {}).get("spec_sha256", "n/a"))[:16]) + r"}); the gate does not move."''',
     r'''             r"The pre-registration's specification is frozen by hash (\texttt{" + _tt4(str(_pf4.get("spec_sha256", "n/a"))[:16]) + r"}); the document, by \texttt{" + _tt4(str((_pff4.get("json") or {}).get("sha256", "n/a"))[:16])
             + r"} (JSON) and \texttt{" + _tt4(str((_pff4.get("md") or {}).get("sha256", "n/a"))[:16]) + r"} (MD); the gate does not move."'''),
]
for fn, pairs in (("artigo_pt_v384.pysnip", PT), ("artigo_en_v384.pysnip", EN)):
    p = os.path.join(HERE, fn); raw = open(p, "rb").read(); s = raw.decode("utf-8")
    assert open(p + ".bak_antes_afer4", "rb").read() == raw
    for old, new in pairs:
        c = s.count(old); assert c == 1, (fn, c, old[:140])
        s = s.replace(old, new)
    b = s.encode("utf-8"); open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)
    print("ok", fn, len(pairs))
