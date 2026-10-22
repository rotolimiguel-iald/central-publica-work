# -*- coding: utf-8 -*-
"""As correcoes da 3a afericao nos trechos do artigo (PT e EN, em paridade): a frase do T1 (o espectro de K sorteado e entregue; o expoente NAO e'
sorteado: a lei injetada e' a raiz, o N3 injeta a linear); o ruido do T1 com as estimativas sem solucao finita ditas; a CPU sem ponto comparavel e
a independencia so na algebra linear; n(c2) so como informacao; o CCI do D128 nao definido fora do modo matematico; a falha do resumo visivel; a
razao de nao ir ao cache; os estatutos [ONTO] (o Nome como matriz, a face matricial, a morte termica) e «o atrator» no lugar de «o Nome como estado»;
a janela como «ao menos um ponto»; o E8; a caixa do veredito sem o allowbreak redundante (o TXT guarda o veredito como um token)."""
import os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))

COMMON_HELPERS_OLD = r'''    _med4 = lambda sg_: max([((v_.get("median_beta_rel_err") or {}).get(sg_)) for v_ in (_t1.get("per_d") or {}).values() if _fin4((v_.get("median_beta_rel_err") or {}).get(sg_))] or [None])'''
COMMON_HELPERS_NEW = r'''    _tx4 = lambda x_: "".join({"\\": r"\textbackslash{}", "{": r"\{", "}": r"\}", "_": r"\_", "%": r"\%", "#": r"\#", "&": r"\&", "$": r"\$", "^": r"\^{}", "~": r"\~{}"}.get(c_, c_) for c_ in str(x_)[:200])

    def _t1nz4(sg_):
        # a maior mediana FINITA entre as dimensoes e, a parte, as dimensoes com estimativas sem solucao finita (3a afericao: nada descartado em silencio)
        fin_ = []; nf_ = []
        for d_, v_ in sorted((_t1.get("per_d") or {}).items(), key=lambda kv_: int(kv_[0]) if str(kv_[0]).isdigit() else 0):
            m_ = (v_.get("median_beta_rel_err") or {}).get(sg_); k_ = (v_.get("n_nonfinite_beta") or {}).get(sg_) or 0; n_ = (v_.get("n_by_sigma") or {}).get(sg_) or 0
            if _fin4(m_):
                fin_.append(m_)
            if k_:
                nf_.append((d_, int(k_), int(n_)))
        return (max(fin_) if fin_ else None), nf_'''

PT = [
    (COMMON_HELPERS_OLD, COMMON_HELPERS_NEW),
    (r'''                if (_reuse4 and _ok4) else ((r"Nesta rodada o mundo quântico foi \textbf{calculado} (chave \texttt{" + _tt4(_q4.get("key")) + r"})"
                                             + (r"; as versões intermediárias seguintes podem reaproveitá-lo por essa chave, e a versão final roda completa, sempre. " if (_q4.get("reuse") or {}).get("saved_to_cache") else r". ")''',
     r'''                if (_reuse4 and _ok4) else ((r"Nesta rodada o mundo quântico foi \textbf{calculado} (chave \texttt{" + _tt4(_q4.get("key")) + r"})"
                                             + (r"; as versões intermediárias seguintes podem reaproveitá-lo por essa chave, e a versão final roda completa, sempre. " if (_q4.get("reuse") or {}).get("saved_to_cache")
                                                else ((r"; não foi guardado para reaproveitamento (" + _tx4((_q4.get("reuse") or {}).get("not_cached_because") or (_q4.get("reuse") or {}).get("cache_error")) + r"). ")
                                                      if ((_q4.get("reuse") or {}).get("not_cached_because") or (_q4.get("reuse") or {}).get("cache_error")) else r". "))'''),
    (r'''             + r"O operador lê o resgate da Relatividade Geral como a prova cosmológica da teoria \textsf{[DECLARADO]} (declaração de 02/10/2026); a régua do programa mantém o que sempre manteve: não falsificado não é confirmado. "
             r"O mundo quântico é a face matricial do mesmo sistema --- \textsf{[COMPUTED]}: cálculo, não medição da natureza ---, com selo próprio ao lado do gate, que não muda.")''',
     r'''             + ((r"\textbf{Os números desta rodada não puderam ser resumidos para o artigo} (\texttt{" + _tx4(_q4.get("summary_error")) + r"}); o veredito e o resultado estão no selo e em \texttt{um\_absoluto\_pilar\_quantico.json}. ") if _q4.get("summary_error") else "")
             + r"O operador lê o resgate da Relatividade Geral como a prova cosmológica da teoria \textsf{[DECLARADO]} (declaração de 02/10/2026); a régua do programa mantém o que sempre manteve: não falsificado não é confirmado. "
             r"Lido pela gerência, o mundo quântico é a face matricial do mesmo sistema \textsf{[ONTO]}; o que a GPU faz é cálculo \textsf{[COMPUTED]}, não medição da natureza, com selo próprio ao lado do gate, que não muda.")'''),
    (r'''$\Pi$ é o projetor do núcleo canônico --- o Nome como matriz). ''', r'''$\Pi$ é o projetor do núcleo canônico --- o Nome como matriz \textsf{[ONTO]}). '''),
    (r'''             r"O estado estacionário $\rho_{ss}$ é o atrator --- o Nome como estado ---, e o seu peso no núcleo é $\mathrm{CCI}=\mathrm{Tr}\,\Pi\rho_{ss}$. "''',
     r'''             r"O estado estacionário $\rho_{ss}$ é o atrator (a leitura «a inscrição que habita o Nome» é \textsf{[ONTO]}), e o seu peso no núcleo é $\mathrm{CCI}=\mathrm{Tr}\,\Pi\rho_{ss}$. "'''),
    (r'''             r"Antes de tudo, o motor confere seis modelos de resposta analítica (amortecimento, \emph{dephasing} puro, a lei-raiz exata, o estimador cego, o qubit térmico, a inversão do tempo) e o piso do estimador: "''',
     r'''             r"Antes de tudo, o motor confere seis modelos de resposta analítica (amortecimento, \emph{dephasing} puro, a lei-raiz exata, o estimador cego, o qubit térmico, a inversão do tempo), o piso do estimador e o comparador da referência na CPU: "'''),
    (r'''r"); entre os pontos de atrator único, o atrator guarda ao menos metade do peso em $\Pi$ numa janela da grade em " + _i4(_t2.get("name_in_core_configs")) + r" das " + _i4(_t2.get("configs")) +
                 r" configurações, e a janela das dobras $n(c^1)\in[2{,}5;\,3{,}5]$ e $n(c^2)\in[1{,}5;\,2{,}5]$ --- na prática, quase-pureza do atrator --- existe em " + _i4(_t2.get("folds_window_configs")) + r" das " + _i4(_t2.get("configs")) + r". "''',
     r'''r"); há ao menos um ponto de atrator único da grade (os pontos não precisam ser contíguos) em que o atrator guarda ao menos metade do peso em $\Pi$ em " + _i4(_t2.get("name_in_core_configs")) + r" das " + _i4(_t2.get("configs")) +
                 r" configurações, e um com as dobras $n(c^1)\in[2{,}5;\,3{,}5]$ e $n(c^2)\in[1{,}5;\,2{,}5]$ --- na prática, quase-pureza do atrator --- em " + _i4(_t2.get("folds_window_configs")) + r" das " + _i4(_t2.get("configs")) + r". "'''),
    (r'''r" injeções em que $\bTGL$, o expoente da lei, o banho e $J$ são sorteados; o estimador recebe só o propagador do sistema inteiro, $\tau$, o espectro de $K$ (a forma da teoria) e $\gamma_{\rm anti}$, não vê $\bTGL$ nem o expoente, e os devolve''',
     r'''r" injeções em que $n_c$, $\bTGL$, o espectro de $K$ na periferia, o banho e $J$ são sorteados (a lei injetada é a raiz, expoente $1/2$; o controle N3 injeta a linear); o estimador recebe só o propagador do sistema inteiro, $\tau$, o espectro de $K$ injetado e $\gamma_{\rm anti}$, não vê $\bTGL$ nem o expoente, e os devolve'''),
    (r'''r" das injeções; com ruído de $10^{-10}$ e $10^{-8}$ no propagador, num subconjunto, a maior mediana do erro relativo de $\bTGL$ entre as dimensões é $" + _e4(_med4("1e-10")) + r"$ e $" + _e4(_med4("1e-08")) + r"$ (curva de resolução, sem decidir). "''',
     r'''r" das injeções; com ruído de $10^{-10}$ e $10^{-8}$ no propagador, num subconjunto, a maior mediana finita do erro relativo de $\bTGL$ entre as dimensões é $" + _e4(_t1nz4("1e-10")[0]) + r"$ e $" + _e4(_t1nz4("1e-08")[0]) + r"$ (curva de resolução, sem decidir)"
                 + "".join((r"; a $" + sg_l + r"$, sem solução finita em " + ", ".join(r"$d=" + str(d_) + r"$: " + str(k_) + r" de " + str(n_) for d_, k_, n_ in _t1nz4(sg_)[1])) for sg_, sg_l in (("1e-10", r"10^{-10}"), ("1e-08", r"10^{-8}")) if _t1nz4(sg_)[1]) + r". "'''),
    (r'''--- a morte térmica é ponto fixo --- em''', r'''--- a morte térmica é ponto fixo \textsf{[ONTO]} --- em'''),
    (r'''        _cpu4 = (r"concorda" if _cr4.get("ok") else (r"\textbf{não estava presente}" if (not _cr4 or _cr4.get("error")) else (r"\textbf{não é desta rodada ou não terminou}" if (_cr4.get("meta_ok") is False or _cr4.get("child_rc") not in (0, None)) else r"\textbf{discorda}")))''',
     r'''        _cpu4 = (r"concorda" if _cr4.get("ok") else (r"\textbf{não estava presente}" if (not _cr4 or _cr4.get("error")) else (r"\textbf{não é desta rodada ou não terminou}" if (_cr4.get("meta_ok") is False or _cr4.get("child_rc") not in (0, None))
                 else (r"\textbf{não pôde comparar nenhum ponto} (todos perto do limiar do gap: nem discordância, nem conferência)" if _cr4.get("not_comparable") else r"\textbf{discorda}"))))'''),
    (r'''r"}, $\mathrm{CCI}=" + _f4(_d8.get("cci"), 4) + r"$, espectro inteiro em "''',
     r'''r"}, " + ((r"$\mathrm{CCI}=" + _f4(_d8.get("cci"), 4) + r"$") if _fin4(_d8.get("cci")) else r"CCI não definido") + r", espectro inteiro em "'''),
    (r'''                 r"Uma referência independente na CPU recalculou " + _i4(_cr4.get("compared")) + r" pontos do T2 (" + _i4(_cr4.get("near_threshold_not_compared")) + r" perto do limiar do gap, relatados e não comparados) e " + _cpu4 + r" (maior diferença de CCI $" + _e4((_cr4.get("max_diffs") or {}).get("cci")) + r"$).")''',
     r'''                 r"Uma referência na CPU, independente na álgebra linear (numpy/LAPACK, processo à parte, com a mesma construção dos operadores), leu " + _i4(_cr4.get("read")) + r" pontos do T2, comparou " + _i4(_cr4.get("compared")) + r" (" + _i4(_cr4.get("near_threshold_not_compared")) + r" perto do limiar do gap, relatados e não comparados) e " + _cpu4 + r" (maior diferença de CCI $" + _e4((_cr4.get("max_diffs") or {}).get("cci")) + r"$; $n(c^2)$ só como informação).")'''),
    (r'''    s.append(r"\begin{center}\small\texttt{" + _tt4(_v4 or "TGL_QUANTUM_PILLAR_V1__ABSENT").replace(r"\_\_", r"\_\_\allowbreak ") + r"}\end{center}")''',
     r'''    s.append(r"\begin{center}\small\texttt{" + _tt4(_v4 or "TGL_QUANTUM_PILLAR_V1__ABSENT") + r"}\end{center}")   # \_ ja quebra no PDF (o preambulo); o TXT guarda o veredito como um token'''),
]

EN = [
    (COMMON_HELPERS_OLD, COMMON_HELPERS_NEW),
    (r'''                if (_reuse4 and _ok4) else ((r"In this run the quantum world was \textbf{computed} (key \texttt{" + _tt4(_q4.get("key")) + r"})"
                                             + (r"; the following intermediate versions may reuse it by that key, and the final version always runs in full. " if (_q4.get("reuse") or {}).get("saved_to_cache") else r". ")''',
     r'''                if (_reuse4 and _ok4) else ((r"In this run the quantum world was \textbf{computed} (key \texttt{" + _tt4(_q4.get("key")) + r"})"
                                             + (r"; the following intermediate versions may reuse it by that key, and the final version always runs in full. " if (_q4.get("reuse") or {}).get("saved_to_cache")
                                                else ((r"; it was not stored for reuse (" + _tx4((_q4.get("reuse") or {}).get("not_cached_because") or (_q4.get("reuse") or {}).get("cache_error")) + r"). ")
                                                      if ((_q4.get("reuse") or {}).get("not_cached_because") or (_q4.get("reuse") or {}).get("cache_error")) else r". "))'''),
    (r'''             + r"The operator reads the recovery of General Relativity as the cosmological proof of the theory \textsf{[DECLARED]} (declaration of 2026-10-02); the program's rule keeps what it always kept: not falsified is not confirmed. "
             r"The quantum world is the matrix face of the same system --- \textsf{[COMPUTED]}: computation, not a measurement of nature ---, with its own seal beside the gate, which does not move.")''',
     r'''             + ((r"\textbf{This run's numbers could not be summarized for the article} (\texttt{" + _tx4(_q4.get("summary_error")) + r"}); the verdict and the result are in the seal and in \texttt{um\_absoluto\_pilar\_quantico.json}. ") if _q4.get("summary_error") else "")
             + r"The operator reads the recovery of General Relativity as the cosmological proof of the theory \textsf{[DECLARED]} (declaration of 2026-10-02); the program's rule keeps what it always kept: not falsified is not confirmed. "
             r"As read by the management, the quantum world is the matrix face of the same system \textsf{[ONTO]}; what the GPU does is computation \textsf{[COMPUTED]}, not a measurement of nature, with its own seal beside the gate, which does not move.")'''),
    (r'''$\Pi$ is the projector onto the canonical core --- the Name as a matrix). ''', r'''$\Pi$ is the projector onto the canonical core --- the Name as a matrix \textsf{[ONTO]}). '''),
    (r'''             r"The stationary state $\rho_{ss}$ is the attractor --- the Name as a state ---, and its weight in the core is $\mathrm{CCI}=\mathrm{Tr}\,\Pi\rho_{ss}$. "''',
     r'''             r"The stationary state $\rho_{ss}$ is the attractor (the reading ``the inscription that dwells in the Name'' is \textsf{[ONTO]}), and its weight in the core is $\mathrm{CCI}=\mathrm{Tr}\,\Pi\rho_{ss}$. "'''),
    (r'''             r"Before anything else the engine checks six models with analytic answers (amplitude damping, pure dephasing, the exact root law, the blind estimator, the thermal qubit, time reversal) and the estimator's floor: "''',
     r'''             r"Before anything else the engine checks six models with analytic answers (amplitude damping, pure dephasing, the exact root law, the blind estimator, the thermal qubit, time reversal), the estimator's floor and the comparator of the CPU reference: "'''),
    (r'''r"); among the points with a unique attractor, the attractor keeps at least half of its weight in $\Pi$ over a window of the grid in " + _i4(_t2.get("name_in_core_configs")) + r" of the " + _i4(_t2.get("configs")) +
                 r" configurations, and the window of the folds $n(c^1)\in[2.5,\,3.5]$ and $n(c^2)\in[1.5,\,2.5]$ --- in practice, near-purity of the attractor --- exists in " + _i4(_t2.get("folds_window_configs")) + r" of the " + _i4(_t2.get("configs")) + r". "''',
     r'''r"); there is at least one grid point with a unique attractor (the points need not be contiguous) where the attractor keeps at least half of its weight in $\Pi$ in " + _i4(_t2.get("name_in_core_configs")) + r" of the " + _i4(_t2.get("configs")) +
                 r" configurations, and one with the folds $n(c^1)\in[2.5,\,3.5]$ and $n(c^2)\in[1.5,\,2.5]$ --- in practice, near-purity of the attractor --- in " + _i4(_t2.get("folds_window_configs")) + r" of the " + _i4(_t2.get("configs")) + r". "'''),
    (r'''r" injections in which $\bTGL$, the exponent of the law, the bath and $J$ are drawn; the estimator receives only the propagator of the whole system, $\tau$, the spectrum of $K$ (the theory's form) and $\gamma_{\rm anti}$, does not see $\bTGL$ or the exponent, and returns them''',
     r'''r" injections in which $n_c$, $\bTGL$, the periphery spectrum of $K$, the bath and $J$ are drawn (the injected law is the root, exponent $1/2$; the N3 control injects the linear one); the estimator receives only the propagator of the whole system, $\tau$, the injected spectrum of $K$ and $\gamma_{\rm anti}$, does not see $\bTGL$ or the exponent, and returns them'''),
    (r'''r" of the injections; with noise of $10^{-10}$ and $10^{-8}$ on the propagator, on a subset, the largest median relative error of $\bTGL$ across dimensions is $" + _e4(_med4("1e-10")) + r"$ and $" + _e4(_med4("1e-08")) + r"$ (a resolution curve, not deciding). "''',
     r'''r" of the injections; with noise of $10^{-10}$ and $10^{-8}$ on the propagator, on a subset, the largest finite median relative error of $\bTGL$ across dimensions is $" + _e4(_t1nz4("1e-10")[0]) + r"$ and $" + _e4(_t1nz4("1e-08")[0]) + r"$ (a resolution curve, not deciding)"
                 + "".join((r"; at $" + sg_l + r"$, no finite solution in " + ", ".join(r"$d=" + str(d_) + r"$: " + str(k_) + r" of " + str(n_) for d_, k_, n_ in _t1nz4(sg_)[1])) for sg_, sg_l in (("1e-10", r"10^{-10}"), ("1e-08", r"10^{-8}")) if _t1nz4(sg_)[1]) + r". "'''),
    (r'''--- heat death is a fixed point --- in''', r'''--- heat death is a fixed point \textsf{[ONTO]} --- in'''),
    (r'''        _cpu4 = (r"agrees" if _cr4.get("ok") else (r"\textbf{was not present}" if (not _cr4 or _cr4.get("error")) else (r"\textbf{is not from this run or did not finish}" if (_cr4.get("meta_ok") is False or _cr4.get("child_rc") not in (0, None)) else r"\textbf{disagrees}")))''',
     r'''        _cpu4 = (r"agrees" if _cr4.get("ok") else (r"\textbf{was not present}" if (not _cr4 or _cr4.get("error")) else (r"\textbf{is not from this run or did not finish}" if (_cr4.get("meta_ok") is False or _cr4.get("child_rc") not in (0, None))
                 else (r"\textbf{could not compare any point} (all near the gap threshold: neither disagreement nor check)" if _cr4.get("not_comparable") else r"\textbf{disagrees}"))))'''),
    (r'''r"}, $\mathrm{CCI}=" + _f4(_d8.get("cci"), 4) + r"$, full spectrum in "''',
     r'''r"}, " + ((r"$\mathrm{CCI}=" + _f4(_d8.get("cci"), 4) + r"$") if _fin4(_d8.get("cci")) else r"CCI undefined") + r", full spectrum in "'''),
    (r'''                 r"An independent CPU reference recomputed " + _i4(_cr4.get("compared")) + r" points of T2 (" + _i4(_cr4.get("near_threshold_not_compared")) + r" near the gap threshold, reported and not compared) and " + _cpu4 + r" (largest CCI difference $" + _e4((_cr4.get("max_diffs") or {}).get("cci")) + r"$).")''',
     r'''                 r"A CPU reference, independent in the linear algebra (numpy/LAPACK, a separate process, with the same construction of the operators), read " + _i4(_cr4.get("read")) + r" points of T2, compared " + _i4(_cr4.get("compared")) + r" (" + _i4(_cr4.get("near_threshold_not_compared")) + r" near the gap threshold, reported and not compared) and " + _cpu4 + r" (largest CCI difference $" + _e4((_cr4.get("max_diffs") or {}).get("cci")) + r"$; $n(c^2)$ for information only).")'''),
    (r'''    s.append(r"\begin{center}\small\texttt{" + _tt4(_v4 or "TGL_QUANTUM_PILLAR_V1__ABSENT").replace(r"\_\_", r"\_\_\allowbreak ") + r"}\end{center}")''',
     r'''    s.append(r"\begin{center}\small\texttt{" + _tt4(_v4 or "TGL_QUANTUM_PILLAR_V1__ABSENT") + r"}\end{center}")   # \_ already breaks in the PDF (preamble); the TXT keeps the verdict as one token'''),
]

for fn, pairs in (("artigo_pt_v384.pysnip", PT), ("artigo_en_v384.pysnip", EN)):
    p = os.path.join(HERE, fn); raw = open(p, "rb").read(); s = raw.decode("utf-8")
    bak = p + ".bak_antes_afer3"
    if not os.path.exists(bak):
        open(bak, "wb").write(raw)
    assert open(bak, "rb").read() == raw
    for old, new in pairs:
        c = s.count(old); assert c == 1, (fn, c, old[:140])
        s = s.replace(old, new)
    assert "_med4" not in s, fn
    b = s.encode("utf-8")
    open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)
    print("ok", fn, len(pairs), "trocas", len(raw), "->", len(b))
