# -*- coding: utf-8 -*-
"""Disposicoes da afericao de CODIGO da v385 nas frases do artigo (artigo_pt_v385.pysnip / artigo_en_v385.pysnip):
 nota 6: a leitura do resultado anterior e' «logo depois de lancar o trabalhador, antes que o calculo novo pudesse substitui-lo» (nao «antes do calculo»);
   o nome do degrau final impresso e' o LIDO do kernel (final_step_name_from_kernel);
 nota 7: F(t) = e^{-tH_min} nao e' termo deste kernel: [KNOWN] (H_min idempotente), com a peca da bancada nomeada (exp_complement_idempotent, nao ligada);
 o comparador novo: a escala max(1,|a|,|b|) (max_scaled_diff), o D128 excluido (dito) e as entradas diferentes (nao comparado).
Pares contados; backup de bytes; compile() de cada trecho como corpo de funcao."""
import os, sys, time, textwrap
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
st = time.strftime("%Y%m%d_%H%M%S")


def aplica(nome, pares):
    P = os.path.join(HERE, nome)
    s0 = open(P, encoding="utf-8", newline="").read(); s = s0
    for a, b in pares:
        n = s.count(a)
        assert n == 1, (nome, "a troca nao e unica", n, a[:100])
        s = s.replace(a, b)
    compile("def _f(core, s):\n" + s, nome, "exec")
    open(P + ".bak_" + st + "_afer1", "wb").write(s0.encode("utf-8"))
    open(P + ".tmp", "w", encoding="utf-8", newline="").write(s); os.replace(P + ".tmp", P)
    print("OK", nome, len(pares), "trocas")


aplica("artigo_pt_v385.pysnip", [
    (r'''o fluxo $F(t)=P+e^{-t}(1-P)=e^{-tH_{\mathrm{min}}}$ satisfaz''',
     r'''o fluxo $F(t)=P+e^{-t}(1-P)$ satisfaz'''),
    (r'''No lock da luz, o que $F$ deixa fixo para todo $t$''',
     r'''Que $F(t)$ seja $e^{-tH_{\mathrm{min}}}$ é conhecido para $H_{\mathrm{min}}$ idempotente \textsf{[KNOWN]}, não termo deste kernel (a bancada tem a peça \texttt{exp\_complement\_idempotent}, ainda não ligada). No lock da luz, o que $F$ deixa fixo para todo $t$'''),
    (r'''    s.append(r"\begin{center}\small\texttt{" + _tt5(_ax5.get("final_step_name") or "AXIOMA__ABSENT") + r"}\end{center}")''',
     r'''    s.append(r"\begin{center}\small\texttt{" + _tt5((_ax5.get("final_step_name_from_kernel") if _ok5 else _ax5.get("final_step_name")) or "AXIOMA__ABSENT") + r"}\end{center}")'''),
    (r'''antes do cálculo, o programa leu o resultado guardado pela rodada anterior e, depois, comparou os dois campo a campo, fora os de tempo e de ambiente: "''',
     r'''logo depois de lançar o trabalhador, antes que o cálculo novo pudesse substituí-lo, o programa leu o resultado guardado pela rodada anterior e, no fim, comparou os dois campo a campo, fora os de tempo e de ambiente, com a escala $\max(1,|a|,|b|)$ do comparador da bancada (campo não finito que difere conta como diferença): "'''),
    (r'''((r"iguais a menos de arredondamento em " + str(_rp5.get("n_fields")) + r" campos (" + str(_rp5.get("n_differ")) + r" diferem; diferença relativa máxima $" + _e5(_rp5.get("max_rel_diff")) + r"$).") if "WITHIN_ROUNDOFF" in _rv5 else''',
     r'''((r"iguais a menos de arredondamento em " + str(_rp5.get("n_fields")) + r" campos (" + str(_rp5.get("n_differ")) + r" diferem; diferença máxima na escala $" + _e5(_rp5.get("max_scaled_diff")) + r"\le10^{-9}$).") if "WITHIN_ROUNDOFF" in _rv5 else'''),
    (r'''                  (r"não houve comparação nesta rodada (" + _tx5(_rp5.get("why") or "sem registro") + r")."))))''',
     r'''                  (r"não houve comparação nesta rodada (" + _tx5(_rp5.get("why") or "sem registro") + r")."))))
             + (r" Os campos do D128 ficaram fora da comparação: o D128 não rodou nesta rodada e rodou na anterior." if _rp5.get("d128_excluded") else "")'''),
])
aplica("artigo_en_v385.pysnip", [
    (r'''the flow $F(t)=P+e^{-t}(1-P)=e^{-tH_{\mathrm{min}}}$ satisfies''',
     r'''the flow $F(t)=P+e^{-t}(1-P)$ satisfies'''),
    (r'''On the light's lock, what $F$ leaves fixed for every $t$''',
     r'''That $F(t)$ is $e^{-tH_{\mathrm{min}}}$ is known for idempotent $H_{\mathrm{min}}$ \textsf{[KNOWN]}, not a term of this kernel (the bench has the piece \texttt{exp\_complement\_idempotent}, not yet linked). On the light's lock, what $F$ leaves fixed for every $t$'''),
    (r'''    s.append(r"\begin{center}\small\texttt{" + _tt5(_ax5.get("final_step_name") or "AXIOMA__ABSENT") + r"}\end{center}")''',
     r'''    s.append(r"\begin{center}\small\texttt{" + _tt5((_ax5.get("final_step_name_from_kernel") if _ok5 else _ax5.get("final_step_name")) or "AXIOMA__ABSENT") + r"}\end{center}")'''),
    (r'''before the computation the program read the result stored by the previous run and, afterwards, compared both field by field, except the time and environment fields: "''',
     r'''right after launching the worker, before the new computation could replace it, the program read the result stored by the previous run and, at the end, compared both field by field, except the time and environment fields, on the scale $\max(1,|a|,|b|)$ of the bench comparator (a non-finite field that differs counts as a difference): "'''),
    (r'''((r"identical up to round-off in " + str(_rp5.get("n_fields")) + r" fields (" + str(_rp5.get("n_differ")) + r" differ; maximum relative difference $" + _e5(_rp5.get("max_rel_diff")) + r"$).") if "WITHIN_ROUNDOFF" in _rv5 else''',
     r'''((r"identical up to round-off in " + str(_rp5.get("n_fields")) + r" fields (" + str(_rp5.get("n_differ")) + r" differ; maximum scaled difference $" + _e5(_rp5.get("max_scaled_diff")) + r"\le10^{-9}$).") if "WITHIN_ROUNDOFF" in _rv5 else'''),
    (r'''                  (r"there was no comparison in this run (" + _tx5(_rp5.get("why") or "no record") + r")."))))''',
     r'''                  (r"there was no comparison in this run (" + _tx5(_rp5.get("why") or "no record") + r")."))))
             + (r" The D128 fields were left out of the comparison: D128 did not run in this run and ran in the previous one." if _rp5.get("d128_excluded") else "")'''),
])
