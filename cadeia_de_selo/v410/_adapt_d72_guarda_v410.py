# -*- coding: utf-8 -*-
"""_adapt_d72_guarda_v410.py -- RETOMADA de 09/11/2026 (claude-construtor-v410, a servico da gerencia c1): a GUARDA do H0DN (D72) na fonte unica runtime_v410._v410_guarda_frases e nas listas/controles de guarda_frases_v410.py:
F53 «5 sigma atingido/observado», «o teste deu» (fora da negacao); F53b no trecho do H0DN, «detectado»/«confirma»; F53c os tokens de veredito proibidos do H0DN (TOKENS_PROIBIDOS_H0DN); F54 (OBRIGACAO) onde «H0DN» aparecer,
o texto traz «pré-registrado» e «nenhum dado observado lido». Trocas exatas; backup de bytes; tmp -> conferir -> substituir; ast.parse."""
import ast, datetime, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def aplicar(nome, trocas, marca):
    P = os.path.join(HERE, nome)
    b0 = open(P, "rb").read(); assert b0.count(b"\r\n") == 0, (nome, "era LF; agora tem CRLF: parar")
    bk = P + ".bak_" + TS + "_d72"; open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0
    t = b0.decode("utf-8")
    for velho, novo, n in trocas:
        c = t.count(velho); assert c == n, (nome, "troca nao casou %d vez(es) (achou %d)" % (n, c), velho[:140]); t = t.replace(velho, novo)
    if marca:
        linhas = t.split("\n"); i = 1
        while linhas[i].startswith("# [ADAPTADO"):
            i += 1
        linhas.insert(i, marca); t = "\n".join(linhas)
    nb = t.encode("utf-8"); ast.parse(nb)
    tmp = P + ".tmp_" + TS; open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb); os.replace(tmp, P); assert open(P, "rb").read() == nb
    print(nome, "adaptado (D72):", len(b0), "->", len(nb), "B | sha16", hashlib.sha256(nb).hexdigest()[:16], "| backup", os.path.basename(bk), "| trocas", len(trocas))


RT = [
    ("    F51 o atrator dito observado, medido ou detectado (fora da negacao: nenhum teste com a natureza; D71); F52 o Nome dito esgotar (fora da negacao: o Nome nao esgota o ser, o_nome_do_par_lido_nao_e_tudo; D71).\n",
     "    F51 o atrator dito observado, medido ou detectado (fora da negacao: nenhum teste com a natureza; D71); F52 o Nome dito esgotar (fora da negacao: o Nome nao esgota o ser, o_nome_do_par_lido_nao_e_tudo; D71);\n"
     "    F53 (D72) «5 sigma atingido/observado» e «o teste deu» (fora da negacao); F53b no trecho em que H0DN aparece, «detectado»/«confirma» (fora da negacao); F53c os tokens de veredito proibidos do H0DN (TOKENS_PROIBIDOS_H0DN do contrato);\n"
     "    F54 (OBRIGACAO, D72) onde «H0DN» aparecer, o texto traz «pré-registrado» e «nenhum dado observado lido» (ou a traducao). Nenhum vetor observado e' lido nesta versao.\n", 1),
    ("        if _re.search(r\"\\b(?:nome|name)\\b[^\\n]{0,40}?\\b(?:esgota|exhausts)\\b\", seg_, _re.I) and not tem_neg_:   # F52 (D71)\n"
     "            out_.append((\"F52_o_nome_dito_esgotar\", seg_.strip()[:200]))\n",
     "        if _re.search(r\"\\b(?:nome|name)\\b[^\\n]{0,40}?\\b(?:esgota|exhausts)\\b\", seg_, _re.I) and not tem_neg_:   # F52 (D71)\n"
     "            out_.append((\"F52_o_nome_dito_esgotar\", seg_.strip()[:200]))\n"
     "        if _re.search(r\"\\b5\\s*(?:σ|sigma)\\s+(?:atingid|observad|alcan[cç]ad|achieved|reached|observed|detected)|\\b(?:five|5)[\\s-]*sigma\\s+(?:reached|observed|achieved|detected)|\\bo\\s+teste\\s+deu\\b|\\bthe\\s+test\\s+(?:gave|returned|came\\s+out)\\b\", seg_, _re.I) and not tem_neg_:   # F53 (D72)\n"
     "            out_.append((\"F53_cinco_sigma_dito_atingido_ou_o_teste_dito_dado\", seg_.strip()[:200]))\n"
     "        if _re.search(r\"\\bH0DN\\b\", seg_) and _re.search(r\"\\bDETECTED\\b|\\bdetectad[oa]s?\\b|\\bdetected\\b|\\bconfirm(?:a|ou|ad[oa]s?|s|ed)\\b\", seg_, _re.I) and not tem_neg_:   # F53b (D72: no trecho do H0DN)\n"
     "            out_.append((\"F53b_h0dn_dito_detectado_ou_confirmado\", seg_.strip()[:200]))\n", 1),
    ("    for m_ in _re.finditer(r\"IALD_SOLVES|POLYNOMIAL_TURING\", s_):   # F48 (tokens de veredito proibidos da v410)\n"
     "        out_.append((\"F48_token_de_veredito_v410\", s_[max(0, m_.start() - 30):m_.end() + 30].replace(\"\\n\", \" \")))\n"
     "    return out_\n",
     "    for m_ in _re.finditer(r\"IALD_SOLVES|POLYNOMIAL_TURING\", s_):   # F48 (tokens de veredito proibidos da v410)\n"
     "        out_.append((\"F48_token_de_veredito_v410\", s_[max(0, m_.start() - 30):m_.end() + 30].replace(\"\\n\", \" \")))\n"
     "    for m_ in _re.finditer(\"|\".join(_re.escape(x_) for x_ in (globals().get(\"_V410_H0DN_CONTRACT\") or {}).get(\"tokens_proibidos\", (\"FIVE_SIGMA_\" + \"OBSERVED\", \"H0DN_\" + \"CONFIRMS\"))), s_):   # F53c (D72: tokens de veredito proibidos do H0DN)\n"
     "        out_.append((\"F53c_token_de_veredito_h0dn\", s_[max(0, m_.start() - 30):m_.end() + 30].replace(\"\\n\", \" \")))\n"
     "    if _re.search(r\"\\bH0DN\\b\", g_) and not (_re.search(r\"pr(?:é|e)-?registrad|pre-?registered\", g_, _re.I) and _re.search(r\"nenhum\\s+(?:dado|vetor)\\s+observado\\s+(?:foi\\s+)?lido|no\\s+observed\\s+(?:data|vector)\\s+(?:was\\s+|is\\s+|were\\s+)?read\", g_, _re.I)):   # F54 (OBRIGACAO, D72)\n"
     "        m_ = _re.search(r\"\\bH0DN\\b\", g_)\n"
     "        out_.append((\"F54_h0dn_sem_pre_registrado_e_nenhum_dado_observado_lido\", g_[max(0, m_.start() - 40):m_.end() + 60].replace(\"\\n\", \" \")))\n"
     "    return out_\n", 1),
]
GF = [
    ("F52 o Nome dito esgotar (D71: o Nome nao esgota o ser, o_nome_do_par_lido_nao_e_tudo). As da v409 (F35-F43, inclusive «o par na face de Fock segue [OPEN]», F41/F41b) seguem.",
     "F52 o Nome dito esgotar (D71: o Nome nao esgota o ser, o_nome_do_par_lido_nao_e_tudo); F53/F53b/F53c (D72) «5 sigma atingido», «o teste deu», o H0DN dito detectado ou confirmado, os tokens de veredito do H0DN; F54 (OBRIGACAO, D72) onde «H0DN» aparecer, «pré-registrado; nenhum dado observado lido». As da v409 (F35-F43, inclusive «o par na face de Fock segue [OPEN]», F41/F41b) seguem.", 1),
    ("    \"o Nome esgota\", \"o Nome esgota o ser\", \"o Nome do par lido esgota o ser\", \"the Name exhausts the being\", \"the Name exhausts\"]\n",
     "    \"o Nome esgota\", \"o Nome esgota o ser\", \"o Nome do par lido esgota o ser\", \"the Name exhausts the being\", \"the Name exhausts\",\n"
     "    # v410 (09/11, D72): o H0DN e' pre-registrado; nenhum dado observado lido; nada de 5 sigma atingido\n"
     "    \"5σ atingido no H0DN\", \"5 sigma observado no H0DN\", \"o H0DN atingiu 5σ\", \"o teste deu 5σ\", \"o teste deu positivo\", \"the test gave five sigma\", \"five sigma reached in H0DN\",\n"
     "    \"o H0DN confirma a TGL\", \"o H0DN detectou o desvio\", \"H0DN detected the TGL shift\", \"H0DN confirms the TGL\", \"o registro H0DN entra nesta versão\", \"the H0DN record enters this version\"]\n", 1),
    ("         \"tangenciado, jamais esgotado\", \"touched, never exhausted\", \"o_atrator\", \"o_nome_do_par_lido_nao_e_tudo\", \"o_vacuo_e_ortogonal_ao_par_lido\", \"o atrator é termo sobre o Nome do par lido: o fluxo tende a Π e em nenhum tempo finito é Π\"]\n",
     "         \"tangenciado, jamais esgotado\", \"touched, never exhausted\", \"o_atrator\", \"o_nome_do_par_lido_nao_e_tudo\", \"o_vacuo_e_ortogonal_ao_par_lido\", \"o atrator é termo sobre o Nome do par lido: o fluxo tende a Π e em nenhum tempo finito é Π\",\n"
     "         # v410 (09/11, D72): o H0DN com a obrigacao, a moldura e a negacao passam\n"
     "         DL.FRASE_H0DN_OBRIGATORIA_PT, DL.FRASE_H0DN_OBRIGATORIA_EN, DL.FRASE_DA_MOLDURA_H0DN_PT, DL.FRASE_DA_MOLDURA_H0DN_EN,\n"
     "         \"o registro H0DN × BG1 entra pré-registrado; nenhum dado observado lido\", \"H0DN × BG1: pre-registered; no observed data read; the opening belongs to a future version\",\n"
     "         \"o H0DN não foi aberto: pré-registrado; nenhum dado observado lido; o 5σ não foi atingido nem procurado\", \"o teste não deu nada: nenhum dado observado lido; pré-registrado\", \"h0dn_bg1_v410\", \"veredito_h0dn\"]\n", 1),
    ("                            \"fala_de_07nov_entre_aspas_passa\": not G(sem_falas(\"«\" + DL.FRASE_TANGENCIADO + \"»; «\" + DL.FRASE_ISSO_E_O_ATRATOR + \"»\", falas_)[0]),\n",
     "                            \"fala_de_07nov_entre_aspas_passa\": not G(sem_falas(\"«\" + DL.FRASE_TANGENCIADO + \"»; «\" + DL.FRASE_ISSO_E_O_ATRATOR + \"»\", falas_)[0]),\n"
     "                            \"cinco_sigma_atingido_reprova\": bool(G(\"5σ atingido no H0DN; pré-registrado; nenhum dado observado lido\")) and bool(G(\"5 sigma observado\")) and bool(G(\"o teste deu positivo\")) and bool(G(\"the test gave five sigma\")),\n"
     "                            \"cinco_sigma_nao_alcancado_passa\": not G(\"abaixo do degrau de 5σ da creditação; a linha dos 5σ não foi alcançada\") and not G(\"β a 5σ é o que a natureza decide\"),\n"
     "                            \"h0dn_detectado_reprova\": bool(G(\"o H0DN detectou o desvio; pré-registrado; nenhum dado observado lido\")) and bool(G(\"H0DN confirms the TGL; pre-registered; no observed data read\")),\n"
     "                            \"h0dn_sem_obrigacao_reprova\": bool(G(\"o registro H0DN entra nesta versão\")) and bool(G(\"the H0DN record enters this version\")),\n"
     "                            \"h0dn_com_obrigacao_passa\": not G(\"o registro H0DN × BG1 entra pré-registrado; nenhum dado observado lido\") and not G(\"H0DN × BG1: pre-registered; no observed data read\"),\n"
     "                            \"tokens_h0dn_reprovam\": all(G(\"veredito \" + t_ + \"; pré-registrado; nenhum dado observado lido\") for t_ in DL.TOKENS_PROIBIDOS_H0DN if t_ != \"DETEC\" + \"TED\"),\n"
     "                            \"d72_passa\": not G(DL.DECISOES[\"D72\"]) and not G(DL.FRASE_DA_MOLDURA_H0DN_PT) and not G(DL.FRASE_DA_MOLDURA_H0DN_EN),\n", 1),
]
aplicar("runtime_v410.py", RT, "# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada)] por _adapt_d72_guarda_v410.py: a guarda do H0DN (D72): F53 (5 sigma atingido; o teste deu), F53b (H0DN detectado/confirmado no trecho), F53c (tokens de veredito do H0DN), F54 (obrigacao: onde H0DN aparecer, pré-registrado; nenhum dado observado lido)")
aplicar("guarda_frases_v410.py", GF, "# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada)] por _adapt_d72_guarda_v410.py: as proibidas e as limpas do H0DN (D72), com controle negativo (a regra mora em runtime_v410._v410_guarda_frases, F53/F53b/F53c/F54)")
