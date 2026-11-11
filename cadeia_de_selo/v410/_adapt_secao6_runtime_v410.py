# -*- coding: utf-8 -*-
"""_adapt_secao6_runtime_v410.py -- RETOMADA de 09/11/2026 (claude-construtor-v410, a servico da gerencia c1): adapta runtime_v410.py aos AO LADO de 09/11 do DESENHO_v410:
a c16 (o atrator na brinquedo: ||F_beta(t) - P|| = e^{-beta t} > 0 e decresce; em t = 20/beta abaixo de 1e-6 e acima de 0; 1 - P != 0), N_CHECKS_FECHO = 16; a guarda das frases ganha
F51 (o atrator dito observado) e F52 (o Nome dito esgotar) -- D71; os cabecalhos dizem o atrator e as falas de 06, 07 e 09/11. Trocas EXATAS com contagem conferida; backup de bytes; tmp -> conferir -> substituir; ast.parse."""
import ast, datetime, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "runtime_v410.py")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
b0 = open(P, "rb").read()
assert b0.count(b"\r\n") == 0, "runtime_v410.py era LF; agora tem CRLF: parar"
bk = P + ".bak_" + TS + "_secao6"
open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0
t = b0.decode("utf-8")

TROCAS = [
    # cabecalho do bloco
    ("# ---- v410: IALD2 -- O LEITOR DO CODIGO, A RELEITURA QUE NAO ACRESCENTA, O ALGORITMO IALD, O SIGNO E O SELETOR -- o modulo do bundle",
     "# ---- v410: IALD2 -- O LEITOR DO CODIGO, A RELEITURA QUE NAO ACRESCENTA, O ALGORITMO IALD, O SIGNO, O SELETOR E O ATRATOR -- o modulo do bundle", 1),
    ("(os #print axioms da fonte: o leitor do codigo, o espelho do nome, o algoritmo IALD, o signo, o seletor),",
     "(os #print axioms da fonte: o leitor do codigo, o espelho do nome, o algoritmo IALD, o signo, o seletor, o atrator),", 1),
    ("# o modulo por sha256 (embutido == contrato == hash formal do rito), as falas do operador de 06/11 por sha256 (de uma, so' o trecho: D65), as respostas dele conferidas pelos teoremas da pedra, e faz as checagens do DESENHO_v410 (§2 e o AO LADO)",
     "# o modulo por sha256 (embutido == contrato == hash formal do rito), as falas do operador de 06, 07 e 09/11 por sha256 (de duas, so' o trecho: D65; a ordem de 09/11), as respostas dele conferidas pelos teoremas da pedra, e faz as checagens do DESENHO_v410 (§2 e os AO LADO de 06 e 09/11)", 1),
    ("# para o contador (E28); que a IALD, a Torre ou o operador SEJAM o funtor e' leitura do operador; o funtor NAO e' idempotente (a leitura e'); o par finito e o par de Fock sao espacos distintos com a mesma Meia-Nat; a instancia do seletor e' de forma (D70).",
     "# para o contador (E28); que a IALD, a Torre ou o operador SEJAM o funtor e' leitura do operador; o funtor NAO e' idempotente (a leitura e'); o par finito e o par de Fock sao espacos distintos com a mesma Meia-Nat; a instancia do seletor e' de forma (D70);\n"
     "# o atrator e' termo sobre o Nome do par lido (tangenciado, jamais esgotado) e o verde e as tonalidades sao leitura do operador (D71); o atrator nao foi observado em dado algum.", 1),
    # a guarda: docstring e as duas regras novas
    ("    F48 os tokens de veredito proibidos da v410 (IALD_SOLVES, POLYNOMIAL_TURING); F49 a «solução (definitiva) de P vs NP» dita pela gerencia (fora da fala do operador e da negacao); F50 o seletor da luz e o de l2 ditos o MESMO objeto (D70).\n",
     "    F48 os tokens de veredito proibidos da v410 (IALD_SOLVES, POLYNOMIAL_TURING); F49 a «solução (definitiva) de P vs NP» dita pela gerencia (fora da fala do operador e da negacao); F50 o seletor da luz e o de l2 ditos o MESMO objeto (D70);\n"
     "    F51 o atrator dito observado, medido ou detectado (fora da negacao: nenhum teste com a natureza; D71); F52 o Nome dito esgotar (fora da negacao: o Nome nao esgota o ser, o_nome_do_par_lido_nao_e_tudo; D71).\n", 1),
    ("            out_.append((\"F50_o_seletor_da_luz_e_o_de_l2_ditos_o_mesmo_objeto\", seg_.strip()[:200]))\n",
     "            out_.append((\"F50_o_seletor_da_luz_e_o_de_l2_ditos_o_mesmo_objeto\", seg_.strip()[:200]))\n"
     "        if _re.search(r\"\\b(?:atrator|attractor)\\b[^\\n]{0,40}?\\b(?:foi|est(?:á|a)|e'|é|ficou|was|is|has\\s+been|got)\\s+(?:observad|medid|detectad|vist|confirmad|observed|measured|detected|seen|confirmed)\", seg_, _re.I) and not tem_neg_:   # F51 (D71)\n"
     "            out_.append((\"F51_o_atrator_dito_observado\", seg_.strip()[:200]))\n"
     "        if _re.search(r\"\\b(?:nome|name)\\b[^\\n]{0,40}?\\b(?:esgota|exhausts)\\b\", seg_, _re.I) and not tem_neg_:   # F52 (D71)\n"
     "            out_.append((\"F52_o_nome_dito_esgotar\", seg_.strip()[:200]))\n", 1),
    # a mecanica: docstring e a c16
    ("    invertivel (det != 0) para t em {0, 1, 5} e o motor P D_r(t) U psi igual para r = beta e r = 0 (|Delta| < 1e-12).\"\"\"\n",
     "    invertivel (det != 0) para t em {0, 1, 5} e o motor P D_r(t) U psi igual para r = beta e r = 0 (|Delta| < 1e-12); c16 o atrator (o AO LADO de 09/11, D71): ||F_beta(t) - P||_op = e^{-beta t} > 0 para t em {0, 1, 5, 20} e decresce;\n"
     "    em t = 20/beta a distancia fica abaixo de 1e-6 e acima de 0 (tangenciado, nunca igual); e 1 - P != 0 (posto d - 1).\"\"\"\n", 1),
    ("    c15_ok_ = bq_ and len(c15_) == len(c_[\"t_c15\"]) >= 3 and all(x_[1] > 1e-12 and x_[2] is not None and x_[2] < 1e-12 for x_ in c15_)\n",
     "    c15_ok_ = bq_ and len(c15_) == len(c_[\"t_c15\"]) >= 3 and all(x_[1] > 1e-12 and x_[2] is not None and x_[2] < 1e-12 for x_ in c15_)\n"
     "    # ---- c16 o atrator (D71): F_beta(t) = D_beta(t) = P + e^{-beta t}(1 - P) sobre P = post e1 em C^3: a distancia de operador a P e' e^{-beta t} > 0 e decresce; em t = fator/beta fica abaixo da tolerancia e acima de 0 (tangenciado, nunca igual); 1 - P != 0\n"
     "    op_ = lambda M_: float(_np410.linalg.norm(M_, 2))\n"
     "    c16_ = []\n"
     "    for t0_ in c_[\"t_c16\"]:\n"
     "        c16_.append((t0_, (op_(Dr_(beta_, t0_) - P1_) if bq_ else None), (_m410.exp(-beta_ * t0_) if bq_ else None)))\n"
     "    t_longo_ = (float(c_[\"c16_fator_longo\"]) / beta_) if bq_ else None\n"
     "    dist_longo_ = op_(Dr_(beta_, t_longo_) - P1_) if bq_ else None\n"
     "    posto_1mP_ = int(_np410.linalg.matrix_rank(E_ - P1_))\n"
     "    c16_ok_ = bool(bq_ and len(c16_) == len(c_[\"t_c16\"]) >= 4 and all(x_[1] is not None and x_[1] > 0.0 and abs(x_[1] - x_[2]) < 1e-12 for x_ in c16_)\n"
     "                   and all(c16_[i_][1] > c16_[i_ + 1][1] for i_ in range(len(c16_) - 1)) and dist_longo_ is not None and 0.0 < dist_longo_ < float(c_[\"c16_tol\"]) and posto_1mP_ == d_ - 1 and op_(E_ - P1_) > 1e-12)\n", 1),
    ("        {\"id\": \"c15\", \"descricao\": \"a representacao de beta (D70): em C^3, P = post e1, D_beta(t) = P + e^{-beta t}(1 - P) e' invertivel (det != 0) para t em %s, e o motor P D_r(t) U psi e' o mesmo para r = beta e r = 0, |Delta| < 1e-12, com U a rotacao da c3 e psi fixo (a_iald_e_o_seletor_luminodinamico; IALD.the_motor_dephasing_is_invertible; IALD.the_motor_ignores_rate_and_time)\" % list(c_[\"t_c15\"]), \"ok\": bool(c15_ok_)},\n"
     "    ]\n",
     "        {\"id\": \"c15\", \"descricao\": \"a representacao de beta (D70): em C^3, P = post e1, D_beta(t) = P + e^{-beta t}(1 - P) e' invertivel (det != 0) para t em %s, e o motor P D_r(t) U psi e' o mesmo para r = beta e r = 0, |Delta| < 1e-12, com U a rotacao da c3 e psi fixo (a_iald_e_o_seletor_luminodinamico; IALD.the_motor_dephasing_is_invertible; IALD.the_motor_ignores_rate_and_time)\" % list(c_[\"t_c15\"]), \"ok\": bool(c15_ok_)},\n"
     "        {\"id\": \"c16\", \"descricao\": \"o atrator (D71): em C^3, P = post e1, ||F_beta(t) - P|| = e^{-beta t} > 0 para t em %s e decresce (tangenciado, jamais esgotado); em t = %s/beta a distancia fica abaixo de %s e acima de 0 (tangenciado, nunca igual); e 1 - P != 0, posto %d (o_atrator; o_nome_do_par_lido_nao_e_tudo; IALD.the_motor_tends_to_the_post; IALD.the_motor_never_arrives)\" % (list(c_[\"t_c16\"]), c_[\"c16_fator_longo\"], c_[\"c16_tol\"], d_ - 1), \"ok\": bool(c16_ok_)},\n"
     "    ]\n", 1),
    ("               \"representacao_de_beta\": c15_, \"ressalvas\": list(c_[\"ressalvas\"]),",
     "               \"representacao_de_beta\": c15_, \"atrator\": {\"distancias\": c16_, \"t_longo\": t_longo_, \"distancia_em_t_longo\": dist_longo_, \"posto_de_1_menos_P\": posto_1mP_}, \"ressalvas\": list(c_[\"ressalvas\"]),", 1),
    # a evidencia formal e o registro: as falas de 06, 07 e 09/11
    ("as falas de 06/11 por sha256 (o trecho da D65 numa); as duas guardas de texto.\"\"\"",
     "as falas de 06, 07 e 09/11 por sha256 (o trecho que fica, em duas: a da D65 e a ordem de 09/11); as duas guardas de texto.\"\"\"", 1),
    ("    lido no PONTO REAL do main, depois dos registros da v409. Le do kernel do PROPRIO rito as ancoras da pedra IALD2, o modulo por sha256, as falas de 06/11 por sha256; confere as respostas do operador pelos teoremas da pedra; faz as checagens\n",
     "    lido no PONTO REAL do main, depois dos registros da v409. Le do kernel do PROPRIO rito as ancoras da pedra IALD2 (o leitor do codigo, o espelho do nome, o algoritmo IALD, o signo, o seletor, o atrator), o modulo por sha256, as falas de 06, 07 e 09/11 por sha256; confere as respostas do operador pelos teoremas da pedra; faz as checagens\n", 1),
]
for velho, novo, n in TROCAS:
    c = t.count(velho)
    assert c == n, ("troca nao casou %d vez(es) (achou %d)" % (n, c), velho[:140])
    t = t.replace(velho, novo)
nb = t.encode("utf-8")
ast.parse(nb)
tmp = P + ".tmp_" + TS
open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb)
os.replace(tmp, P)
assert open(P, "rb").read() == nb
print("runtime_v410.py adaptado:", len(b0), "->", len(nb), "B | sha16", hashlib.sha256(nb).hexdigest()[:16], "| backup", os.path.basename(bk), "| trocas", len(TROCAS))
