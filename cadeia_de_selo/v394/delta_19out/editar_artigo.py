# -*- coding: utf-8 -*-
"""editar_artigo.py -- DELTA 19/10: acrescenta aos .pysnip da v394 (PT e EN; backup de bytes ja' feito) UM paragrafo, antes dos «Limites», sobre o criterio binario de parada: o texto LE o registro criterio_binario_de_parada_v394
do core (selou ou NAO selou) e nao digita numero. Passa pela guarda P18 e pelo ast.parse no gerar_candidato_v394.py. Cada troca tem assert de unicidade."""
import ast, os
V = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PT_ANCORA = '    s.append(r"\\textbf{Limites.} '
EN_ANCORA = '    s.append(r"\\textbf{Limits.} '
PT = '''    _cb394 = core.get("criterio_binario_de_parada_v394") or {}
    if _cb394:
        s.append(r"\\textbf{O critério binário de parada (delta de 19/10).} A pedra candidata \\texttt{TheBinaryReadingAtTheFixedPoint} (nome provisório: o operador nomeia) compõe, por citação e sem matemática nova, oito teoremas que já estavam no kernel: as duas faces $P_+$ e $P_-$ partem a identidade e a leitura de ambas é total sobre a forma; reler não acrescenta; as duas faces do absoluto pesam $\\frac{1}{2}$ cada; a meia-nat sai da simetria de $J$; no ponto fixo não há transição mudada e a iteração é estável; e a entropia do bit justo ($\\ln 2$) não é a meia-nat. "
                 r"A analogia com um sistema quântico sobre 1 e 0 vale nos pesos $(\\frac{1}{2},\\frac{1}{2})$, não na entropia. O registro \\texttt{criterio\\_binario\\_de\\_parada\\_v394} " + (r"selou neste rito: " if _cb394.get("all_verified") is True else r"NÃO selou neste rito: ")
                 + r"a bandeira da pedra e os oito teoremas lidos do kernel do rito, dentro do trio, e as duas falas do operador de 19/10 embutidas por sha256. \\textsf{[ONTO]} A leitura «a parada é o ponto fixo» e a TGL binária (o positivo, o negativo e a leitura de ambos) são do operador; o kernel entrega a forma estrutural, não um procedimento de decisão. Validade no kernel não é creditação, e o gate não se move.")
'''
EN = '''    _cb394 = core.get("criterio_binario_de_parada_v394") or {}
    if _cb394:
        s.append(r"\\textbf{The binary stopping criterion (19 Oct delta).} The candidate stone \\texttt{TheBinaryReadingAtTheFixedPoint} (provisional name: the operator names it) composes, by citation and with no new mathematics, eight theorems already in the kernel: the two faces $P_+$ and $P_-$ split the identity and the reading of both is total on the form; re-reading adds nothing; the two faces of the absolute weigh $\\frac{1}{2}$ each; the half-nat comes out of the symmetry of $J$; at the fixed point there is no changed transition and the iteration is stable; and the entropy of the fair bit ($\\ln 2$) is not the half-nat. "
                 r"The analogy with a quantum system over 1 and 0 holds on the weights $(\\frac{1}{2},\\frac{1}{2})$, not on the entropy. The record \\texttt{criterio\\_binario\\_de\\_parada\\_v394} " + (r"sealed in this rite: " if _cb394.get("all_verified") is True else r"did NOT seal in this rite: ")
                 + r"the flag of the stone and the eight theorems read from the kernel of the rite, within the trio, and the two operator statements of 19 Oct embedded by sha256. \\textsf{[ONTO]} The reading ``the stop is the fixed point'' and the binary TGL (the positive, the negative and the reading of both) are the operator's; the kernel delivers the structural form, not a decision procedure. Validity in the kernel is not creditation, and the gate does not move.")
'''
for nome, ancora, bloco in (("artigo_pt_v394.pysnip", PT_ANCORA, PT), ("artigo_en_v394.pysnip", EN_ANCORA, EN)):
    p = os.path.join(V, nome); t = open(p, "rb").read().decode("utf-8")
    assert "criterio_binario_de_parada_v394" not in t, "ja' editado"
    assert t.count(ancora) == 1, (nome, t.count(ancora))
    t = t.replace(ancora, bloco + ancora)
    ast.parse("def _f(core, verdict, data_path, s):\n" + t)
    open(p + ".tmp", "wb").write(t.encode("utf-8")); os.replace(p + ".tmp", p)
    print(nome, "ok", len(t.encode("utf-8")))
