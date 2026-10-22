# -*- coding: utf-8 -*-
"""Disposicoes da TERCEIRA passada de afericao da v385 (afericao_passada3\\RELATORIO_AFERIDOR_PASSADA3_v385.txt):
 CORRIGIR: o conferidor de citacoes promete so o que garante («mensagem de entrada do operador, sem bloco colado MARCADO») e grava, por citacao, o carimbo e
   o tamanho da mensagem onde acha (leitura humana);
 N1: o conferidor do rito compara tambem os NUMEROS do registro da reprodutibilidade no selo com os do core (nao so o veredito);
 N2: o token diz beta > 0 E contraste > 0 (o g do kernel: «β > 0 e contraste > 0», NoFullWitness.lean:88);
 N3: no EN, «on ker T» (nao «on the kernel», homonimo do kernel Lean);
 N4: «bit a bit» literal -- mesmo tipo e mesmo float.hex; valor igual com representacao diferente vai a arredondamento (diferenca 0), dito;
 N5: o teste de unidade do token NOT_COMPARED_THIS_RUN_DID_NOT_COMPUTE_A_RESULT, e o de 3 contra 3.0.
Pares contados; backup de BYTES; temporario -> conferir -> substituir; ast.parse / compile."""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
st = time.strftime("%Y%m%d_%H%M%S")


def aplica(nome, pares, modo="py"):
    P = os.path.join(HERE, nome)
    b0 = open(P, "rb").read(); s = b0.decode("utf-8")
    for a, b in pares:
        n = s.count(a)
        assert n == 1, (nome, "a troca nao e unica", n, a[:100])
        s = s.replace(a, b)
    if modo == "py":
        ast.parse(s)
    else:
        compile("def _f(core, s):\n" + s, nome, "exec")
    open(P + ".bak_" + st + "_p3", "wb").write(b0)
    nb = s.encode("utf-8"); open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb); os.replace(P + ".tmp", P)
    print("OK", nome, len(pares), "trocas")


aplica("v385_runtime.py", [
    ("THE_ZERO_IS_THE_FALSE_WITNESS_THE_FULL_STATIC_WITNESS_FORBIDDEN_BY_BETA_THE_ABSOLUTE_ZERO_UNREACHABLE_IN_FINITE_TIME__",
     "THE_ZERO_IS_THE_FALSE_WITNESS_THE_FULL_STATIC_WITNESS_FORBIDDEN_BY_BETA_AND_CONTRAST_THE_ABSOLUTE_ZERO_UNREACHABLE_IN_FINITE_TIME__"),
    ("            if x_ == y_:\n                continue\n            sc = abs(fx - fy)",
     "            if x_ == y_ and type(x_) is type(y_) and (not isinstance(x_, float) or x_.hex() == y_.hex()):   # (3a passada, N4) bit a bit LITERAL: tipo e bits\n"
     "                continue\n            sc = abs(fx - fy)"),
])
aplica("conferir_rito_v385.py", [
    ('and str(rp.get("verdict") or "").startswith("TGL_QUANTUM_PILLAR_REPRODUCIBILITY_V385__") and srp.get("verdict") == rp.get("verdict"),',
     'and str(rp.get("verdict") or "").startswith("TGL_QUANTUM_PILLAR_REPRODUCIBILITY_V385__") and srp.get("verdict") == rp.get("verdict")\n'
     '        and all(srp.get(k_) == rp.get(k_) for k_ in ("compared", "n_fields", "n_differ", "max_scaled_diff", "d128_excluded")),   # (3a passada, N1) os NUMEROS do selo = os do core'),
])
aplica("artigo_en_v385.pysnip", [
    (r"\texttt{verb\_word\_fixes\_the\_name} (on the kernel, the word of the Verb acts as the scalar $q(0)$)",
     r"\texttt{verb\_word\_fixes\_the\_name} (on $\ker T$, the word of the Verb acts as the scalar $q(0)$)"),
], modo="snip")
aplica("ensaio_a_seco_v385.py", [
    ('U["anterior_fora_de_compute"] =',
     '_pr0 = um.quantum_pillar_previous_v385({"mode": "REUSE"})\n'
     'U["sem_calculo_nesta_rodada_token"] = "NOT_COMPARED_THIS_RUN_DID_NOT_COMPUTE_A_RESULT" in um.quantum_pillar_reproducibility_v385(_pr0, _rec)["verdict"]   # (3a passada, N5)\n'
     '_p33 = copy.deepcopy(_prev); _r33 = copy.deepcopy(_rec); _p33["summary"]["T2"]["configs"] = 3; _r33["summary"]["T2"]["configs"] = 3.0\n'
     'U["valor_igual_tipo_diferente_nao_e_bit_a_bit"] = "REPRODUCED_BIT_FOR_BIT" not in um.quantum_pillar_reproducibility_v385(_p33, _r33)["verdict"]   # (3a passada, N4)\n'
     'U["anterior_fora_de_compute"] ='),
])
aplica("conferir_citacoes_v385.py", [
    ('"""Confere, por script, que TODA citacao do operador na v385 esta VERBATIM numa mensagem DELE (a regua nº 1: nunca fabricar citacao; achado 1 da 1a afericao\nde texto e achado 2 da 2a passada):',
     '"""Confere, por script, que toda citacao do operador na v385 esta VERBATIM numa MENSAGEM DE ENTRADA DO OPERADOR, SEM BLOCO COLADO MARCADO (a regua nº 1:\n'
     'nunca fabricar citacao; achado 1 da 1a afericao de texto, achado 2 da 2a passada e o CORRIGIR da 3a: o script NAO distingue texto colado SEM marca dentro\n'
     'da mensagem -- por isso grava, para cada citacao, o carimbo e o TAMANHO da mensagem onde acha, para a leitura humana):'),
    ('            out.append(ts)\n    return out', '            out.append({"quando": ts, "tamanho_da_mensagem": len(m)})\n    return out'),
])
