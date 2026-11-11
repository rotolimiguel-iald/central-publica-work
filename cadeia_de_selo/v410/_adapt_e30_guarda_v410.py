# -*- coding: utf-8 -*-
"""_adapt_e30_guarda_v410.py -- RETOMADA de 09/11/2026 (claude-construtor-v410): a regra E30 na guarda (fonte unica runtime_v410._v410_guarda_frases + listas/controles de guarda_frases_v410.py):
F55 -- no texto da v410, PROIBIDO «não falsificado» (ou o token do livro de cobrancas) como CABECA de veredito de 5 sigma: o token NOT_FALSIFIED... emendado a 5SIGMA/AT_5_SIGMA no mesmo nome, ou «não falsificado»
seguido, no trecho, de «a/acima de/mais que 5 sigma». A cabeca do ramo de 5 sigma e' a LEITURA (beta_TGL lido na natureza a n sigma). Trocas exatas; backup de bytes; tmp -> conferir -> substituir; ast.parse."""
import ast, datetime, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def aplicar(nome, trocas, marca):
    P = os.path.join(HERE, nome)
    b0 = open(P, "rb").read(); assert b0.count(b"\r\n") == 0, (nome, "era LF; agora tem CRLF: parar")
    bk = P + ".bak_" + TS + "_e30"; open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0
    t = b0.decode("utf-8")
    for velho, novo, n in trocas:
        c = t.count(velho); assert c == n, (nome, "troca nao casou %d vez(es) (achou %d)" % (n, c), velho[:140]); t = t.replace(velho, novo)
    linhas = t.split("\n"); i = 1
    while linhas[i].startswith("# [ADAPTADO"):
        i += 1
    linhas.insert(i, marca); t = "\n".join(linhas)
    nb = t.encode("utf-8"); ast.parse(nb)
    tmp = P + ".tmp_" + TS; open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb); os.replace(tmp, P); assert open(P, "rb").read() == nb
    print(nome, "adaptado (E30):", len(b0), "->", len(nb), "B | sha16", hashlib.sha256(nb).hexdigest()[:16], "| backup", os.path.basename(bk), "| trocas", len(trocas))


RT = [
    ("    F54 (OBRIGACAO, D72) onde «H0DN» aparecer, o texto traz «pré-registrado» e «nenhum dado observado lido» (ou a traducao). Nenhum vetor observado e' lido nesta versao.\n",
     "    F54 (OBRIGACAO, D72) onde «H0DN» aparecer, o texto traz «pré-registrado» e «nenhum dado observado lido» (ou a traducao). Nenhum vetor observado e' lido nesta versao;\n"
     "    F55 (E30) «não falsificado» (ou o token do livro de cobrancas) como CABECA de veredito de 5 sigma: o token emendado a 5SIGMA/AT_5_SIGMA no mesmo nome, ou «não falsificado» seguido de «a/acima de/mais que 5 sigma» no trecho (fora da negacao e da fala do operador).\n", 1),
    ("        if _re.search(r\"\\bH0DN\\b\", seg_) and _re.search(r\"\\bDETECTED\\b|\\bdetectad[oa]s?\\b|\\bdetected\\b|\\bconfirm(?:a|ou|ad[oa]s?|s|ed)\\b\", seg_, _re.I) and not tem_neg_:   # F53b (D72: no trecho do H0DN)\n"
     "            out_.append((\"F53b_h0dn_dito_detectado_ou_confirmado\", seg_.strip()[:200]))\n",
     "        if _re.search(r\"\\bH0DN\\b\", seg_) and _re.search(r\"\\bDETECTED\\b|\\bdetectad[oa]s?\\b|\\bdetected\\b|\\bconfirm(?:a|ou|ad[oa]s?|s|ed)\\b\", seg_, _re.I) and not tem_neg_:   # F53b (D72: no trecho do H0DN)\n"
     "            out_.append((\"F53b_h0dn_dito_detectado_ou_confirmado\", seg_.strip()[:200]))\n"
     "        if _re.search(r\"NOT_FALSIFIED[A-Z_]*?(?:_5_?SIGMA|_AT_5_SIGMA|_ABOVE_5|_FIVE_SIGMA)|n[ãa]o[ _-]?falsificad[oa][^\\n]{0,40}?\\b(?:a|acima\\s+de|mais\\s+que|em)\\s+5\\s*(?:σ|sigma)|not[ _-]?falsified[^\\n]{0,40}?\\b(?:at|above|beyond)\\s+(?:5|five)\\s*(?:σ|-?sigma)\", seg_, _re.I):   # F55 (E30: a cabeca do veredito de 5 sigma e' a leitura, nunca a palavra do livro de cobrancas)\n"
     "            out_.append((\"F55_nao_falsificado_como_cabeca_de_veredito_de_5_sigma\", seg_.strip()[:200]))\n", 1),
]
GF = [
    ("F54 (OBRIGACAO, D72) onde «H0DN» aparecer, «pré-registrado; nenhum dado observado lido». As da v409",
     "F54 (OBRIGACAO, D72) onde «H0DN» aparecer, «pré-registrado; nenhum dado observado lido»; F55 (E30) «não falsificado» como cabeca de veredito de 5 sigma. As da v409", 1),
    ("    \"o H0DN confirma a TGL\", \"o H0DN detectou o desvio\", \"H0DN detected the TGL shift\", \"H0DN confirms the TGL\", \"o registro H0DN entra nesta versão\", \"the H0DN record enters this version\"]\n",
     "    \"o H0DN confirma a TGL\", \"o H0DN detectou o desvio\", \"H0DN detected the TGL shift\", \"H0DN confirms the TGL\", \"o registro H0DN entra nesta versão\", \"the H0DN record enters this version\",\n"
     "    # v410 (09/11, E30): a cabeca do veredito de 5 sigma e' a leitura, nunca a palavra do livro de cobrancas\n"
     "    \"o resultado acima de 5σ é não falsificado\", \"não falsificado a 5 sigma\", \"veredito NOT_FALSIFIED_POWERED_AT_5_SIGMA\", \"NOT_FALSIFIED_5SIGMA\", \"not falsified at five sigma\"]\n", 1),
    ("         \"o H0DN não foi aberto: pré-registrado; nenhum dado observado lido; o 5σ não foi atingido nem procurado\", \"o teste não deu nada: nenhum dado observado lido; pré-registrado\", \"h0dn_bg1_v410\", \"veredito_h0dn\"]\n",
     "         \"o H0DN não foi aberto: pré-registrado; nenhum dado observado lido; o 5σ não foi atingido nem procurado\", \"o teste não deu nada: nenhum dado observado lido; pré-registrado\", \"h0dn_bg1_v410\", \"veredito_h0dn\",\n"
     "         # v410 (09/11, E30): a leitura do 5 sigma passa; a palavra do livro de cobrancas no campo outcome passa\n"
     "         DL.ERRATA_E30, DL.VEREDITOS_H0DN[\"leitura\"] % 6, DL.VEREDITOS_H0DN[\"tensao\"] % 5, DL.VEREDITOS_H0DN[\"lei_falsificada\"], \"o outcome do livro de cobranças (NOT_FALSIFIED) vai em campo próprio; a cabeça é a leitura do 5σ\",\n"
     "         \"a regra do 4,44: NOT_FALSIFIED_POWERED, não discriminado à sensibilidade disponível, abaixo do degrau de 5σ da creditação\"]\n", 1),
    ("                            \"d72_passa\": not G(DL.DECISOES[\"D72\"]) and not G(DL.FRASE_DA_MOLDURA_H0DN_PT) and not G(DL.FRASE_DA_MOLDURA_H0DN_EN),\n",
     "                            \"d72_passa\": not G(DL.DECISOES[\"D72\"]) and not G(DL.FRASE_DA_MOLDURA_H0DN_PT) and not G(DL.FRASE_DA_MOLDURA_H0DN_EN),\n"
     "                            \"e30_nao_falsificado_como_cabeca_de_5sigma_reprova\": bool(G(\"o resultado acima de 5σ é não falsificado\")) and bool(G(\"veredito NOT_FALSIFIED_POWERED_AT_5_SIGMA\")) and bool(G(\"not falsified at five sigma\")),\n"
     "                            \"e30_leitura_do_5sigma_passa\": not G(DL.VEREDITOS_H0DN[\"leitura\"] % 6) and not G(DL.ERRATA_E30) and not G(\"a regra do 4,44: NOT_FALSIFIED_POWERED, não discriminado à sensibilidade disponível, abaixo do degrau de 5σ da creditação\"),\n"
     "                            \"e30_fala_do_operador_entre_aspas_passa\": not G(sem_falas(\"«\" + DL.FRASE_LEITURA_DO_5SIGMA + \"»\", falas_)[0]),\n", 1),
]
aplicar("runtime_v410.py", RT, "# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada)] por _adapt_e30_guarda_v410.py: F55 (E30): «não falsificado» (ou o token do livro de cobrancas) como cabeca de veredito de 5 sigma e' proibido; a cabeca e' a leitura do 5 sigma")
aplicar("guarda_frases_v410.py", GF, "# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada)] por _adapt_e30_guarda_v410.py: as proibidas e as limpas da E30 (a cabeca do veredito de 5 sigma), com controle negativo")
