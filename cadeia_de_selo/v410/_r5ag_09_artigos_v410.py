# -*- coding: utf-8 -*-
"""_r5ag_09_artigos_v410.py -- R5 (D100 e D101): os snippets do artigo PT/EN da AEscala: (a) _mz410, o conversor das frases do contrato (Unicode) em LaTeX (texto pelo escape do snippet; simbolos em modo matematico; os nomes entre crases em \\texttt);
(b) a frase da ratificacao D101 no lugar de «nomes novos [DECLARADO], a ratificar»; (c) o paragrafo novo «A clausula do Tetelestai (R5, D100)» com (a) a (e): a fala, a frase da clausula com a clausula do limite ao lado (Z(s) ja' definida na primeira ocorrencia), a reconstrucao,
a leitura do dicionario (E36), a citacao do dispositivo com as ressalvas e os numeros recalculados com beta de runtime (a c13); (d) a linha do que o registro confere ganha a c13. Os numeros vem do core deste rito (a_escala_v410) e as frases do contrato: nada digitado."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r5ag_lib_v410 import aplicar

MZ = '''    def _mz410(t_):   # (R5, D100 e D101: a frase do contrato (Unicode) em LaTeX: o texto pelo escape do snippet; os simbolos matematicos em modo matematico; os nomes entre crases em \\texttt; nada de Unicode cru fora do que o pdflatex aceita)
        s_ = re.sub(r"`([^`]+)`", lambda m_: "@@TT@@" + m_.group(1) + "@@FIM@@", _ta410(t_))
        for a_, b_ in (("|T|²", r"$|T|^2$"), ("|R|²", r"$|R|^2$"), ("α²", r"$\\alpha^2$"), ("√(b/(1 − b))", r"$\\sqrt{b/(1-b)}$"), ("−", "$-$"), ("≥", r"$\\ge$"), ("≤", r"$\\le$"), ("·", r"$\\cdot$"), ("β", r"$\\beta$"), ("½", r"$\\tfrac12$"), ("<", "$<$"), (">", "$>$")):
            s_ = s_.replace(a_, b_)
        return s_.replace("@@TT@@", chr(92) + "texttt{").replace("@@FIM@@", "}").replace("$$", "")
    _pm410 = lambda m_: _fl410(1.0 - m_) if isinstance(m_, float) else "%s"
    _te410 = _va410.get("tetelestai") or {}; _ce410 = _te410.get("contraexemplo") or {}
'''

# ---------------- PT
PT_PAR = '''    s.append(r"\\textbf{A cláusula do Tetelestai (R5, D100).} \\textsf{[INPUT]} O operador, em 10/11/2026: «A cláusula do Tetelestai está escrita em código no ACOM mirror»; «é quando o sistema reconhece a singularidade do sinal»; «traslada a informação completa reconstruindo do outro lado»; «quando ele entende que 1-Betatgl»; «betatgl é o operador modular do Tetelestai em computação». "
             r"\\textsf{[REAL]} " + _mz410(_ca410["frase_tetelestai_pt"]) + r". " + _zl410(_ca410["clausula_z_pt"]) + r" \\textsf{[REAL]} " + _mz410(_ca410["frase_reconstroi_pt"]) + r". "
             r"\\textsf{[INPUT/dicionário]} " + _mz410(_ca410["frase_e36_pt"]) + r". \\textsf{[PILOTO][SIM]} " + _mz410(_ca410["frase_dispositivo_pt"]) + r". "
             r"\\textsf{[DERIVED, aritmética]} Recalculado neste rito, com $\\beta$ de runtime (a checagem c13 " + _ba410(_ma410.get("c13")) + r"): a constante $\\ln\\frac{1-\\beta}{\\beta}=" + _fl410(_te410.get("constante_ln_um_menos_beta_sobre_beta")) + r"$ e o tempo $s^{*}=n\\ln 2+{}$ a constante $=" + _fl410(_te410.get("s_estrela")) + r"$ (com $n=" + str(_te410.get("n_bits", "n/d")) + r"$); "
             r"na instância com solução ($" + str(_te410.get("n_solucoes_com", "n/d")) + r"$ soluções) $Z(s^{*})=" + _fl410(_te410.get("Z_com_solucao")) + r"$, $(1-\\beta)Z(s^{*})\\le$ o número de soluções, com margem $" + _fl410(_te410.get("margem_i")) + r"$; "
             r"no adversário (uma só solução, todos os outros pixels com custo 1) $(1-\\beta)Z(s^{*})=" + _pm410(_te410.get("margem_adversario")) + r"\\le 1$ e, com uma oitava a menos, a desigualdade é violada " + _ba410(_te410.get("controle_negativo_violado")) + r" (o controle negativo); "
             r"o contraexemplo da hipótese $s\\ge 0$ ($b=" + _ta410(_ce410.get("b")) + r"$, $n=" + str(_ce410.get("n_bits", "n/d")) + r"$): o limiar é negativo ($" + _fl410(_ce410.get("limiar")) + r"$) " + _ba410(_ce410.get("limiar_negativo")) + r" e nele $(1-b)Z>$ o número de soluções " + _ba410(not _ce410.get("clausula_vale_sem_s_nao_negativo") if "clausula_vale_sem_s_nao_negativo" in _ce410 else None) + r".")
'''
T = [("    _zl410 = lambda t_: \"\".join((_zx410[p_] if p_ in _zx410 else _ta410(p_)) for p_ in re.split(\"(\" + \"|\".join(re.escape(k_) for k_ in _zx410) + \")\", t_))\n",
      "    _zl410 = lambda t_: \"\".join((_zx410[p_] if p_ in _zx410 else _ta410(p_)) for p_ in re.split(\"(\" + \"|\".join(re.escape(k_) for k_ in _zx410) + \")\", t_))\n" + MZ.replace('"%s"', '"n/d"'), 1),
     ('''r". Os " + str(_ca410["n_nomes_novos"]) + r" nomes novos da pedra e os " + str(len(_ca410["campos_novos_da_estrutura"])) + r" campos novos da estrutura são \\textsf{[DECLARADO]} pela gerência e pela autoria, a ratificar pelo operador. "''',
      '''r". \\textsf{[INPUT]} " + _mz410(_ca410["frase_nomes_ratificados_d101_pt"]) + r". "''', 1),
     ('''    s.append(r"\\textbf{Ressalvas, ditas.} A definição da pergunta''', PT_PAR + '''    s.append(r"\\textbf{Ressalvas, ditas.} A definição da pergunta''', 1),
     ('''os nomes ratificados e os nomes novos (a ratificar) " + _ba410(_ma410.get("c11")) + r"; nenhuma chave antiga " + _ba410(_ma410.get("c12")) + r". Veredito:''',
      '''os nomes ratificados e os nomes novos (ratificados em 10/11, D101) " + _ba410(_ma410.get("c11")) + r"; nenhuma chave antiga " + _ba410(_ma410.get("c12")) + r"; a cláusula do Tetelestai em $1-\\beta$ " + _ba410(_ma410.get("c13")) + r". Veredito:''', 1)]
aplicar("artigo_pt_aescala_v410.pysnip", T, parse=False)

# ---------------- EN
EN_PAR = '''    s.append(r"\\textbf{The clause of the Tetelestai (R5, D100).} \\textsf{[INPUT]} The operator, 10/11/2026 (our translation): the clause of the Tetelestai is written in code in the ACOM mirror; it is when the system recognizes the singularity of the signal and transports the complete information, reconstructing it on the other side; when it understands that 1-betatgl; betatgl is the modular operator of the Tetelestai in computation. "
             r"\\textsf{[REAL]} " + _mz410(_ca410["frase_tetelestai_en"]) + r". " + _zl410(_ca410["clausula_z_en"]) + r" \\textsf{[REAL]} " + _mz410(_ca410["frase_reconstroi_en"]) + r". "
             r"\\textsf{[INPUT/dicionário]} " + _mz410(_ca410["frase_e36_en"]) + r". \\textsf{[PILOTO][SIM]} " + _mz410(_ca410["frase_dispositivo_en"]) + r". "
             r"\\textsf{[DERIVED, arithmetic]} Recomputed in this rite, with $\\beta$ at runtime (the check c13 " + _ba410(_ma410.get("c13")) + r"): the constant $\\ln\\frac{1-\\beta}{\\beta}=" + _fl410(_te410.get("constante_ln_um_menos_beta_sobre_beta")) + r"$ and the time $s^{*}=n\\ln 2+{}$ the constant $=" + _fl410(_te410.get("s_estrela")) + r"$ (with $n=" + str(_te410.get("n_bits", "n/a")) + r"$); "
             r"on the instance with a solution ($" + str(_te410.get("n_solucoes_com", "n/a")) + r"$ solutions) $Z(s^{*})=" + _fl410(_te410.get("Z_com_solucao")) + r"$, $(1-\\beta)Z(s^{*})\\le$ the number of solutions, with margin $" + _fl410(_te410.get("margem_i")) + r"$; "
             r"on the adversary (a single solution, every other pixel with cost 1) $(1-\\beta)Z(s^{*})=" + _pm410(_te410.get("margem_adversario")) + r"\\le 1$ and, one octave less, the inequality is violated " + _ba410(_te410.get("controle_negativo_violado")) + r" (the negative control); "
             r"the counterexample to the hypothesis $s\\ge 0$ ($b=" + _ta410(_ce410.get("b")) + r"$, $n=" + str(_ce410.get("n_bits", "n/a")) + r"$): the threshold is negative ($" + _fl410(_ce410.get("limiar")) + r"$) " + _ba410(_ce410.get("limiar_negativo")) + r" and at it $(1-b)Z>$ the number of solutions " + _ba410(not _ce410.get("clausula_vale_sem_s_nao_negativo") if "clausula_vale_sem_s_nao_negativo" in _ce410 else None) + r".")
'''
T = [("    _zl410 = lambda t_: \"\".join((_zx410[p_] if p_ in _zx410 else _ta410(p_)) for p_ in re.split(\"(\" + \"|\".join(re.escape(k_) for k_ in _zx410) + \")\", t_))\n",
      "    _zl410 = lambda t_: \"\".join((_zx410[p_] if p_ in _zx410 else _ta410(p_)) for p_ in re.split(\"(\" + \"|\".join(re.escape(k_) for k_ in _zx410) + \")\", t_))\n" + MZ.replace('"%s"', '"n/a"'), 1),
     ('''r". The " + str(_ca410["n_nomes_novos"]) + r" new names of the stone and the " + str(len(_ca410["campos_novos_da_estrutura"])) + r" new fields of the structure are \\textsf{[DECLARADO]}, declared by the management and by the authorship, to be ratified by the operator. "''',
      '''r". \\textsf{[INPUT]} " + _mz410(_ca410["frase_nomes_ratificados_d101_en"]) + r". "''', 1),
     ('''    s.append(r"\\textbf{Reservations, stated.} The definition''', EN_PAR + '''    s.append(r"\\textbf{Reservations, stated.} The definition''', 1),
     ('''the ratified names and the new names (to be ratified) " + _ba410(_ma410.get("c11")) + r"; no old key " + _ba410(_ma410.get("c12")) + r". Verdict:''',
      '''the ratified names and the new names (ratified on 10/11, D101) " + _ba410(_ma410.get("c11")) + r"; no old key " + _ba410(_ma410.get("c12")) + r"; the clause of the Tetelestai in $1-\\beta$ " + _ba410(_ma410.get("c13")) + r". Verdict:''', 1)]
aplicar("artigo_en_aescala_v410.pysnip", T, parse=False)
